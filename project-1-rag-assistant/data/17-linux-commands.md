# Linux 常用命令

## 文件操作

ls -la：列出所有文件含隐藏文件
cd：切换目录
pwd：显示当前路径
cp：复制文件或目录
mv：移动或重命名
rm：删除文件，rm -rf 递归强制删除（慎用）

## 权限管理

chmod 755 file：设置文件权限，r=4 w=2 x=1
chown user:group file：更改文件所有者
Linux 权限分三组：所有者、所属组、其他用户

## 进程管理

ps aux：查看所有进程
top/htop：实时进程监控
kill -9 PID：强制终止进程
nohup command &：后台运行不受终端关闭影响集

## 文本处理

grep：文本搜索，grep -r "error" /var/log/
awk：文本分析和格式化
sed：流编辑器，批量替换
tail -f：实时查看文件末尾

## 网络命令

curl：发送 HTTP 请求
wget：下载文件
netstat/ss：查看网络连接
ping：测试连通性
scp：远程拷贝文件
