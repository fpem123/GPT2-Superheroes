FROM leehoseop/gpt2_superheroes:1.1

WORKDIR /app
COPY . .

EXPOSE 80

CMD ["python3", "main.py"]
