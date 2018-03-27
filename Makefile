default: serve

serve:
	dev_appserver.py .

deploy:
	gcloud app deploy . --promote --version `git rev-parse --short HEAD` --project zinc-shard-358
