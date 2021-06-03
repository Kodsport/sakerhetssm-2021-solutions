FROM node:14-alpine
WORKDIR /app/web
COPY src/web ./
RUN npm install
RUN npm run-script build
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
WORKDIR /app
RUN pip install pipenv
COPY src/Pipfile* /app/
RUN pipenv install --system --deploy --ignore-pipfile
COPY src/api.py /app/
COPY src/game/ /app/game/
EXPOSE 8000
COPY --from=0 /app/web/public ./web/public
COPY easy/flag.txt flag0.txt
COPY medium/flag.txt flag1.txt
COPY hard/flag.txt flag2.txt
COPY expert/flag.txt flag3.txt
COPY impossible/flag.txt flag4.txt
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
