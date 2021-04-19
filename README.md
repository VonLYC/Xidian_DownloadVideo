# Xidian_DownloadVideo
众所周知，在你电期末复习的重要手段就是看课程回放，但是由于回放平台的稀烂(指不能快进、容易卡等问题)   
而且到1202年了，还用Flash播放器
故有了这个能够下载回放视频的脚本

# Usages
首先安装相应的库
``` python
pip3 install -r requirements.txt
```
其次，你如果是第一次使用selenium，你需要为你的服务器配置chromedriver，具体请谷歌`selenium chrome环境配置` 

接下来找到你要下载的课程的URL（如下图所示，每一节课都有一个URL）
![(S@WHI4SF6A8 5OM_QE535X](https://user-images.githubusercontent.com/43775038/115207470-36822b00-a12e-11eb-972f-5bd3785cbdaa.png)
最后在download_m3u8_video.py中修改你的Chrome路径地址和下载的课程的URL

![H7{ZI _TMO__`4J77C M4%5](https://user-images.githubusercontent.com/43775038/115208261-f3748780-a12e-11eb-9c4b-5436936bfe14.png)

运行download_m3u8_video.py就行了
