@SET name=parking
@SET app=kozlovsv78/%name%
docker stop %name%
docker build -t %app% .
docker run -d -p 80:80 ^
  --name=%name% ^
  --rm ^
  -v "%CD%":"/app" ^
  -e FLASK_APP=main.py -e FLASK_ENV=development -e FLASK_DEBUG=1 ^
  %app% ^
  flask run --host=0.0.0.0 --port=80