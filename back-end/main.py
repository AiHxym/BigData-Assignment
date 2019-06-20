from pyspark import SparkContext
from flask import Flask, render_template, jsonify
from random import *
from flask import request
import json

# step1:准备数据
sc = SparkContext()
global Path
print('运行在:'+sc.master[0:5],'上')
if sc.master[0:5]=="local":
    # Path="file:/home/hadoop/spark/sparkwork1/"
    Path='data/'
else:
    Path="hdfs://master:9000/user/hduser/"
rawUserData = sc.textFile(Path+"/ml-100k/u.data")
print(rawUserData.count()) #打印数据的行数
print(rawUserData.first()) #first data(userID projectID evaluate Date)
# 准备Als训练数据 导入Rating模块
from pyspark.mllib.recommendation import Rating
rawRatings = rawUserData.map(lambda line:line.split("\t")[:3]) # 只要前三列,并通过\t分割
print(rawRatings.take(5))
# 查看RDD数目
ratingsRDD = rawRatings.map(lambda x:(x[0],x[1],x[2])) # ALS训练数据是RDD类型,所以转换数据未RDD
print(ratingsRDD.take(5)) # 查看前5行
print(ratingsRDD.count()) # 查看数量


users = ratingsRDD.map(lambda x:x[0]).distinct().collect()

# 查看不重复用户数
numUsers = ratingsRDD.map(lambda x:x[0]).distinct().count()
print(numUsers) # 943个用户
# 查看不重复电影数
numMovies = ratingsRDD.map(lambda x:x[1]).distinct().count()
print('不重复电影数',numMovies)

# step2:训练模型
from pyspark.mllib.recommendation import ALS
# ALS训练,采用显示评分
model = ALS.train(ratingsRDD,10,10,0.01) #参数:数据RDD 中间矩阵大小 迭代次数 学习率
print('模型为:',model)

# step3:使用模型进行推荐
print('用户id是100的推荐的5个电影',model.recommendProducts(100,5)) # 参数: 推荐用户id 推荐数目 返回:列表(包括用户id 产品id 评分)
# 查看针对用户推荐产品的评分
print('给用户100推荐1141的评分为:',model.predict(100,1141))
# 针对电影推荐给用户
model.recommendUsers(product=200,num=5)

# step4:显示推荐电影名称
itemRDD = sc.textFile(Path+"/ml-100k/u.item")
print('显示一共有多少电影',itemRDD.count()) # 一共1682个电影
# 创建"电影ID与名称"的字典
movieTitle = itemRDD.map(lambda line:line.split('|')).map(lambda a:(float(a[0]),a[1])).collectAsMap() # 创建一个字典,先划分数据变成RDD类型,然后转换成字典,键是id,值是电影名字
#显示字典的前5项
print('字典:',movieTitle)
# 查询电影名称
print(movieTitle[5])
# 显示前5条推荐电影的名称
recommendP = model.recommendProducts(100,5) # 返回参数 第二个是产品
for p,rec in enumerate(recommendP):
    print('对用户'+str(p)+' 推荐电影'+str(movieTitle[rec.product])+' 推荐评分'+str(rec.rating))

app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")

@app.route('/api/get_users', methods=['POST'])
def get_users():
    return json.dumps(users)

@app.route('/api/get_films', methods=['POST'])
def get_films():
    req_data = json.loads(request.get_data(as_text=True))
    res = {}
    for user in req_data:
        for film in model.recommendProducts(int(user), 20):
            if(film.product in res):
                res[film.product] +=  film.rating
            else:
                res[film.product] = film.rating
    return json.dumps(res)

@app.route('/api/get_film_title', methods=['POST'])
def get_film_title():
    return json.dumps(movieTitle)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


app.run()
