module.exports = {
  runtimeCompiler: true,
  publicPath: '/', // 设置打包文件相对路径
  devServer: {
    // open: process.platform === 'darwin',
    // host: 'localhost',
    port: 8000,
    // open: true, //配置自动启动浏览器
    proxy: {
      '/api': {
        target: 'http://localhost:5000',//后端接口地址
        //changeOrigin: true,//是否允许跨越
        pathRewrite: {
          '^/api': '/api',//重写,
        }
      }
    },
  },
}