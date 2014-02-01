git add .
git commit -m 'update'
git push origin master
make html
cd output && ./deploy.sh