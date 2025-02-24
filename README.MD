# Simple FastAPI Application with Celery [Redis] and SQLAlchemy

## Instructions [for an easier docker setup]:
1. Ensure you have a valid OPENAI_API_KEY in .env file.
2. Run ```docker-compose build```
3. Run ```docker-compose up```
4. The FastAPI server will be up and running, and can be accessed on http://localhost:8000/docs


## Instructions for a non-docker setup:
1. Ensure you have a valid OPENAI_API_KEY in .env file.
2. In a terminal, run the following command: ```docker run --name redis -p 6379:6379 -d redis```
3. Now run the following command: ```pip install -r requirements.txt```
4. Now run the following command: ```celery -A celery_tasks.celery worker --loglevel=info --pool=solo```
5. Open another terminal and run ```uvicorn main:app``` and your FastAPI Server can be accessed on http://localhost:8000/docs

## Points to note:
- The file 'db.db' already has some rows populated for demonstration purposes.
- Code will work even without OPENAI_API_KEY, but missing/null tone and sentiment from the database will not be re-generated by the LLM.