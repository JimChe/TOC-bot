# TOC Project 2020

[![Maintainability](https://api.codeclimate.com/v1/badges/dc7fa47fcd809b99d087/maintainability)](https://codeclimate.com/github/NCKU-CCS/TOC-Project-2020/maintainability)

[![Known Vulnerabilities](https://snyk.io/test/github/NCKU-CCS/TOC-Project-2020/badge.svg)](https://snyk.io/test/github/NCKU-CCS/TOC-Project-2020)


Template Code for TOC Project 2020

A Line bot based on a finite state machine

More details in the [Slides](https://hackmd.io/@TTW/ToC-2019-Project#) and [FAQ](https://hackmd.io/s/B1Xw7E8kN)

## 概述
3C時代，免不了的是每天長時間的低頭與坐著使用電子產品。
由於肌肉長時間處於同樣姿勢，肌肉纖維不斷維持在相同的長度。
肌肉不會變得緊繃的話，你應該是外星人吧。

想避免肌肉緊繃，就要盡量避免長時間維持相同姿勢。
但總是不小心一晃眼時間就過了，肌肉也隨著時間的流逝緊繃起來。
這時可以透過按摩放鬆的方式來舒緩緊繃的肌肉。
舒緩後除了感覺疲勞一消而散，精神也好了許多，工作效率也得到提升了!!!

作者觀察了周遭許多同學、朋友，對於肌肉放鬆有概念的並不多，
於是就想製作一個具有簡易教學以及一些肌肉放鬆小知識的聊天機器人。



## 使用方式
1. 初始狀態是 "user" 模式，可以呼叫 "help" 來觀看下一步可以輸入的指令，或是輸入 "痠痛" 讓機器人詢問你哪邊痠痛，或是輸入 "fsm" 取得fsm圖。
2. 若輸入上述三種關鍵字，可以輸入 "back" 回到 "user" 狀態。
3. 若輸入 "痠痛" ，機器人會請您選擇 "肩頸痠痛" 或是 "背部痠痛"。
4. 選擇後會顯示對應的可能緊繃的肌肉。
5. 可以再輸入 "如何放鬆" ，了解更多細節。
6. 若輸入 "如何放鬆" ，可以選擇觀看 "放鬆用具"(跳出用具圖片) 或是 "放鬆位置"(跳出相關肌肉的位置) 或是 "教學"(跳出文字訊息講解如何放鬆)
7. 若輸入 "還是不懂" ，會跳出相關推薦的影片(技術問題無法直接提供連結...)。
8. 在任何狀態輸入 "restart" ，會回到 "user" 狀態。
9. 在任何狀態輸入 "人體肌肉圖" ，會跳出人體肌肉的解頗圖，上面有各部位肌肉的名稱，觀看後輸入 "back"。回到原先的狀態。



## Setup

### Prerequisite
* Python 3.6
* Pipenv
* Facebook Page and App
* HTTPS Server

#### Install Dependency
```sh
pip3 install pipenv

pipenv --three

pipenv install

pipenv shell
```

* pygraphviz (For visualizing Finite State Machine)
    * [Setup pygraphviz on Ubuntu](http://www.jianshu.com/p/a3da7ecc5303)
	* [Note: macOS Install error](https://github.com/pygraphviz/pygraphviz/issues/100)


#### Secret Data
You should generate a `.env` file to set Environment Variables refer to our `.env.sample`.
`LINE_CHANNEL_SECRET` and `LINE_CHANNEL_ACCESS_TOKEN` **MUST** be set to proper values.
Otherwise, you might not be able to run your code.

#### Run Locally
You can either setup https server or using `ngrok` as a proxy.

#### a. Ngrok installation
* [ macOS, Windows, Linux](https://ngrok.com/download)

or you can use Homebrew (MAC)
```sh
brew cask install ngrok
```

**`ngrok` would be used in the following instruction**

```sh
ngrok http 8000
```

After that, `ngrok` would generate a https URL.

#### Run the sever

```sh
python3 app.py
```

#### b. Servo

Or You can use [servo](http://serveo.net/) to expose local servers to the internet.


## Finite State Machine
http://140.116.102.136:8000/show-fsm

## Usage
The initial state is set to `user`.

Every time `user` state is triggered to `advance` to another state, it will `go_back` to `user` state after the bot replies corresponding message.

* user
	* Input: "go to state1"
		* Reply: "I'm entering state1"

	* Input: "go to state2"
		* Reply: "I'm entering state2"

## Deploy
Setting to deploy webhooks on Heroku.

### Heroku CLI installation

* [macOS, Windows](https://devcenter.heroku.com/articles/heroku-cli)

or you can use Homebrew (MAC)
```sh
brew tap heroku/brew && brew install heroku
```

or you can use Snap (Ubuntu 16+)
```sh
sudo snap install --classic heroku
```

### Connect to Heroku

1. Register Heroku: https://signup.heroku.com

2. Create Heroku project from website

3. CLI Login

	`heroku login`

### Upload project to Heroku

1. Add local project to Heroku project

	heroku git:remote -a {HEROKU_APP_NAME}

2. Upload project

	```
	git add .
	git commit -m "Add code"
	git push -f heroku master
	```

3. Set Environment - Line Messaging API Secret Keys

	```
	heroku config:set LINE_CHANNEL_SECRET=your_line_channel_secret
	heroku config:set LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
	```

4. Your Project is now running on Heroku!

	url: `{HEROKU_APP_NAME}.herokuapp.com/callback`

	debug command: `heroku logs --tail --app {HEROKU_APP_NAME}`

5. If fail with `pygraphviz` install errors

	run commands below can solve the problems
	```
	heroku buildpacks:set heroku/python
	heroku buildpacks:add --index 1 heroku-community/apt
	```

	refference: https://hackmd.io/@ccw/B1Xw7E8kN?type=view#Q2-如何在-Heroku-使用-pygraphviz

## Reference
[Pipenv](https://medium.com/@chihsuan/pipenv-更簡單-更快速的-python-套件管理工具-135a47e504f4) ❤️ [@chihsuan](https://github.com/chihsuan)

[TOC-Project-2019](https://github.com/winonecheng/TOC-Project-2019) ❤️ [@winonecheng](https://github.com/winonecheng)

Flask Architecture ❤️ [@Sirius207](https://github.com/Sirius207)

[Line line-bot-sdk-python](https://github.com/line/line-bot-sdk-python/tree/master/examples/flask-echo)
