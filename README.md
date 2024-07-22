# fastapi_group_project
 Simple fastapi app
 


## DO IT TO RUN:

CL - means Commend line

Use the 'Dockerfile' so that the program can run in a Docker container. Remember to run container before steps below.

1. Create '.env' file in 'fastapi_app' folder.
2. Next, in CL write : poetry shell
3. Confirme by ENTER buttom
4. Next , in CL write : poetry install
5. Confirme by ENTER buttom
6. Then go to 'fastapi_group_project\fastapi_app' and  to create tables in db type in CL: alembic upgrade head
7. Confirme by ENTER buttom
8. Type in CL cd..
9. Confirme by ENTER buttom
10. To enter the correct folder in CL type : cd docs
11. Confirme by ENTER buttom
12. Then, type in CL: .\make.bat html
13. Confirme by ENTER buttom
14. Type in CL cd..
15. Confirme by ENTER buttom
16. To enter the correct folder in CL type : cd fastapi_app
17. Confirme by ENTER buttom
18. To run API server type in CL: uvicorn main:app --host localhost --port 8000 --reload
19. Confirme by ENTER buttom
20. Open a web browser and go to: http://localhost:8000/docs.

## MANUAL

To read documentation about this aplication take a look to the file "fastapi_group_project\docs\_build\html\index.html".