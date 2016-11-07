source appengine-creds.conf # XXX: Local file with credentials
user=djangouser
pass=${password}

git clone https://github.com/GoogleCloudPlatform/appengine-django-skeleton.git
cd appengine-django-skeleton

echo "For safety reasons you must manually create a project through the Google Cloud Console and enable it for billing before continuing"
read project
instance="${project}sql"
"${gcloud}" config set account ${account}
"${gcloud}" auth login
"${gcloud}" config set project ${project}

"${gcloud}" sql instances create ${instance}
"${gcloud}" sql instances patch ${instance} --authorized-networks 0.0.0.0/0
"${gcloud}" sql instances patch ${instance} --assign-ip


echo "Create a user/pass ${user}:${pass} manually" # TODO:
read
#"${gcloud}" beta # XXX: interactive install
"${gcloud}" sql instances set-root-password --password ${password} ${project}
host=`"${gcloud}"  sql instances  describe  ${instance} | grep ' ipAddress:' | awk '{print $3}'` # TODO



db="maindb"
echo "Create a db called ${db} manually" # TODO:
read

sed -ie "s/<your-database-name>/${db}/g" mysite/settings.py
sed -ie "s/<your-database-user>/${user}/g" mysite/settings.py
sed -ie "s/<your-database-password>/${pass}/g" mysite/settings.py
sed -ie "s/<your-database-host>/${host}/g" mysite/settings.py
sed -ie "s/<your-project-id>/${project}/g" mysite/settings.py
sed -ie "s/<your-cloud-sql-instance>/${instance}/g" mysite/settings.py

pip install -r requirements-vendor.txt -t lib/
pip install -r requirements-local.txt

pip install django -y
pip install mysqlclient -y
pip install MySQLdb -y # XXX: Optional depending on OS flavor


python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
appcfg.py update . -A ${project}
