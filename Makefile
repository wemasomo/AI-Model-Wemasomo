build:
	docker build \
  --platform linux/amd64 -t europe-west10-docker.pkg.dev/wagon-bootcamp-428813/wemasomo/masomo_image:prod .

push:
	docker push europe-west10-docker.pkg.dev/wagon-bootcamp-428813/wemasomo/masomo_image:prod

deploy:
	gcloud run deploy wemasomo-app \
    --image europe-west10-docker.pkg.dev/wagon-bootcamp-428813/wemasomo/masomo_image:prod \
    --platform managed \
    --region europe-west10 \
    --allow-unauthenticated --memory 8Gi --cpu 4
