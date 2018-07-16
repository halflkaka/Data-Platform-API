# Data-Platform-API
## 框架
Python+Flask+PyMongo
## 主要功能
1. 用户访问权限验证 2. 数据集动态创建 3. 数据上传和获取
## 测试方法
建立本地mongodb，通过postman输入url和请求方法测试api
## 使用方法
终端中在文件存放位置输入
```
pip install -r requirements.txt
```
输入
```
python app.py
```
启动localhost server。默认端口为5000，数据库默认名为restdb，请确保本地数据库名称与其一致。
安装依赖。
使用API_driver文件夹中已封装的FT_API_Utils.py使用api。API_driver文件夹中的demo.py是一个使用示例。
