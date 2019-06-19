<style scoped>
</style>
<template>
  <div style="display:flex">
    <Card style="width:20%;height:900px;overflow:scroll;text-align:center">
      <p slot="title">
        <Icon type="ios-person"/>Users
      </p>
      <CheckboxGroup v-model="selectedUsers">
        <tr v-for="usercol in users">
          <Checkbox v-for="user in usercol" :label="user">
            <span>{{user}}</span>
          </Checkbox>
        </tr>
      </CheckboxGroup>
    </Card>
    <Card style="width:80%;height:900px;overflow:scroll;text-align:center">
      <p slot="title">
        <Icon type="ios-film-outline"/>Film Recommendation
      </p>
    </Card>
  </div>
</template>
<script>
import axios from "axios";
import qs from "qs";
import { types } from "util";
import { constants } from "crypto";

export default {
  components: {},
  data() {
    return {
      users: [],
      selectedUsers: []
    };
  },
  watch: {
    selectedUsers() {
      this.getFilms();
    }
  },
  created() {
    this.getUsers();
  },
  mounted() {},
  methods: {
    getUsers() {
      const path = "/api/get_users";
      let keep;
      let req = {};
      axios
        .post(path, req)
        .then(response => {
          this.users = response.data.slice();
          let len = this.users.length;
          let n = 6; //假设每行显示4个
          let lineNum = len % n === 0 ? len / n : Math.floor(len / n + 1);
          let res = [];
          for (let i = 0; i < lineNum; i++) {
            // slice() 方法返回一个从开始到结束（不包括结束）选择的数组的一部分浅拷贝到一个新数组对象。且原始数组不会被修改。
            let temp = this.users.slice(i * n, i * n + n);
            res.push(temp);
          }
          this.users = res;
        })
        .catch(error => {
          console.log(error);
        });
    },
    getFilms() {
      const path = "/api/get_films";
      let req = this.selectedUsers;
      axios
        .post(path, req)
        .then(response => {
          console.log(response.data);
          let arr = [];
          Object.keys(response.data).forEach(function(key) {
            arr.push({key: key, value: response.data[key]});
          });
          arr.sort((a,b)=>{
              return b.value - a.value
          });
          
          /*this.users = response.data.slice();
          let len = this.users.length;
          let n = 6; //假设每行显示4个
          let lineNum = len % n === 0 ? len / n : Math.floor(len / n + 1);
          let res = [];
          for (let i = 0; i < lineNum; i++) {
            // slice() 方法返回一个从开始到结束（不包括结束）选择的数组的一部分浅拷贝到一个新数组对象。且原始数组不会被修改。
            let temp = this.users.slice(i * n, i * n + n);
            res.push(temp);
          }
          this.users = res;*/
        })
        .catch(error => {
          console.log(error);
        });
    }
  }
};
</script>
