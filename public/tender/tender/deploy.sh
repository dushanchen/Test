scrapyd命令:

打包:
scrapyd-deploy -p tender -v t-01 --build-egg=egg tender.egg

添加版本:
	 curl http://localhost:6800/addversion.json -F project=myproject -F version=r23 -F egg=@myproject.egg

运行:
 curl http://localhost:6800/schedule.json -d project=myproject -d spider=somespider