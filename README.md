# TaskViewer

### 1.软件说明：
这是一个网页版的任务管理类的工具，主要有两个功能
- 复习工具：根据艾宾浩斯遗忘曲线设计，对所学内容进行复习。可自己修改复习规则，较为灵活方便。
- 任务管理：分为长期任务和短期任务

### 2.环境配置：
- python3.8
- flask              
- flask-mysqldb
- flask-sqlalchemy
- mysql

### 3.使用:
- 建空数据库：task_reviewer
- 打开 setting.py 按照本地参数对数据库进行设置
- DATABASE_INITIALIZATION：第一次需要在数据库中建表，因此该值设为True。随后运行时需要设为False
- REVIEW_RULES和TOTAL_REVIEW_RULES分别用来设置子任务和总任务的复习规则，按照 第i次复习：间隔天数 的规则进行设置
- 运行：python runserver.py

  

