import requests
import json

methodChoice = input('choose method 1.login 2.signup : ')
if methodChoice == '1':
  print("welcome to login")
  name = input("Enter your name: ")
  pw = input("Enter your password: ")
  sendingData = {'name': name, 'password': pw}
  headers = {"Content-Type": "application/json"}
  json_data = json.dumps(sendingData)
  authorizeUser = requests.post('http://10.80.161.234:8000/login/', json_data, headers)
  userinfo = str(authorizeUser)
  if(userinfo.split('[')[1].split(']')[0]=='401'):
    print('error: check your username and password')
  if(userinfo.split('[')[1].split(']')[0]=='200'):
    print('success')
    print()
    print('='*45)
    print(f'welcome back, user "{authorizeUser.json()["name"]}"!')
    print('='*45)
    print()
    getTodoList = requests.get(f'http://10.80.161.234:8000/getTodo/{authorizeUser.json()["user_id"]}', headers=headers)
    if (getTodoList.status_code == 200):
      if getTodoList.json() != []:
        for i in getTodoList.json():
          print(f'''
          
====================
제목: {i['title']}
내용: {i['content']}
상태: {"완료" if i['completed'] else "미완료"}
====================
          
          ''')
      else:
        print('아직 투두가 없습니다.')
    else:
      print('unknown error :', getTodoList)

if methodChoice == '2':
  print("welcome to signup")
  name = input("Enter your name: ")
  pw = input("Enter your password: ")
  sendingData = {'name': name, 'password': pw}
  headers = {"Content-Type": "application/json"}
  json_data = json.dumps(sendingData)

  createUser = requests.post('http://10.80.161.234:8000/signup/', data=json_data, headers=headers)
  userinfo = str(createUser)
  if(userinfo.split('[')[1].split(']')[0]=='422'):
    print('error')
  if(userinfo.split('[')[1].split(']')[0]=='200'):
    print('success')
  AfterSignup = input("Do you wish to login now?(y/n)")
  if(AfterSignup == 'y'):
    print("welcome to login")
    name = input("Enter your name: ")
    pw = input("Enter your password: ")
    sendingData = {'name': name, 'password': pw}
    headers = {"Content-Type": "application/json"}
    json_data = json.dumps(sendingData)

    authorizeUser = requests.post('http://10.80.161.234:8000/login/', data=json_data, headers=headers)
    userinfo = str(authorizeUser)
    if (userinfo.split('[')[1].split(']')[0] == '401'):
      print('error: check your username and password')
    if (userinfo.split('[')[1].split(']')[0] == '200'):
      print('success')
      print(f'welcome back, user "{authorizeUser.json()["name"]}"!')
  else:
    print('See you again!')
    quit()


