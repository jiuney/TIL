# 카카오맵 api 활용하기

서로 다른 동네에 사는 세명이서 한 장소에서 모일 때, 각자로부터 거리가 동일한 한 장소 선택하기.

삼각형의 외심을 생각하면 된다.

## 기초 작업

우선 프로젝트를 담을 `js_kakaomap` 폴더를 생성한다.

```bash
mkdir js_kakaomap
cd js_kakaomap
```

`js_kakaomap` 폴더 안에 `index.html` 생성.

```bash
touch index.html
```

`index.html` 에 기본 골격 만들기.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    
</body>
</html>
```



## 카카오 api 사용하기

[Kakao Developers](https://developers.kakao.com/) 에 카카오아이디로 로그인해서 앱 만들기.

앱 만들면 나오는 앱 키 중에 JavaScript 키 복사해두기.



## 카카오맵 api 사용하기

[Kakao 지도 Web API 가이드](http://apis.map.kakao.com/web/guide/) 페이지에서 '시작하기' 부분 참고해서 지도 영역과 Javascript API, 지도를 띄우는 코드 복사해서 `index.html`에 붙여넣기.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <div id="map" style="width:500px;height:400px;"></div>
    <script type="text/javascript" src="//dapi.kakao.com/v2/maps/sdk.js?appkey=발급받은 APP KEY를 넣으시면 됩니다."></script>
    <script>
        var container = document.getElementById('map'); //지도를 담을 영역의 DOM 레퍼런스
        var options = { //지도를 생성할 때 필요한 기본 옵션
            center: new kakao.maps.LatLng(33.450701, 126.570667), //지도의 중심좌표.
            level: 3 //지도의 레벨(확대, 축소 정도)
        };

        var map = new kakao.maps.Map(container, options); //지도 생성 및 객체 리턴
    </script>
</body>
</html>
```

* "발급받은 APP KEY를 넣으시면 됩니다." 부분에 아까 복사해 둔 키를 붙여넣는다.

`index.html` 에서 오래된 문법을 최근 많이 사용하는 문법(es6 형식)으로 고쳐준다.

```html
...
<script>
    let container = document.querySelector('#map'); //지도를 담을 영역의 DOM 레퍼런스
    let options = { //지도를 생성할 때 필요한 기본 옵션
        center: new kakao.maps.LatLng(33.450701, 126.570667), //지도의 중심좌표.
        level: 3 //지도의 레벨(확대, 축소 정도)
    };

    let map = new kakao.maps.Map(container, options); //지도 생성 및 객체 리턴
</script>
...
```

* var는 let으로 바꿔준다.
* getElementById 도 querySelector 로 바꿔준다.

이제 지도상에서 내가 클릭한 부분에 마커로 표시를 해주려고 한다. 이를 위해 카카오 맵에 이벤트 리스너를 등록한다. `index.html` 수정.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <div id="map" style="width:500px;height:400px;"></div>
    <script type="text/javascript" src="http://dapi.kakao.com/v2/maps/sdk.js?appkey=앱키"></script>
    <script>
        let container = document.querySelector('#map'); //지도를 담을 영역의 DOM 레퍼런스
        let options = { //지도를 생성할 때 필요한 기본 옵션
            center: new kakao.maps.LatLng(33.450701, 126.570667), //지도의 중심좌표.
            level: 3 //지도의 레벨(확대, 축소 정도)
        };

        let map = new kakao.maps.Map(container, options); //지도 생성 및 객체 리턴

        // 카카오 맵에 이벤트 리스너 등록
        kakao.maps.event.addListener(map, 'click', function(mouseEvent) {
            addMarker(mouseEvent.latLng)
        })

        const addMarker = (position) => {
            // 클릭 이벤트를 통해서 들어오는 position 정보를 이용하여 마커 생성
            const marker = new kakao.maps.Marker({
                position
            })
            // 마커를 맵에 표시
            marker.setMap(map)
        }
    </script>
</body>
</html>
```

마커로 표시된 위치를 담는 리스트를 만든다. `index.html` 수정.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <div id="map" style="width:500px;height:400px;"></div>
    <script type="text/javascript" src="http://dapi.kakao.com/v2/maps/sdk.js?appkey=앱키"></script>
    <script>
        let container = document.querySelector('#map'); //지도를 담을 영역의 DOM 레퍼런스
        let options = { //지도를 생성할 때 필요한 기본 옵션
            center: new kakao.maps.LatLng(33.450701, 126.570667), //지도의 중심좌표.
            level: 3 //지도의 레벨(확대, 축소 정도)
        };

        let map = new kakao.maps.Map(container, options); //지도 생성 및 객체 리턴
        const markers = []

        // 카카오 맵에 이벤트 리스너 등록
        kakao.maps.event.addListener(map, 'click', function(mouseEvent) {
            addMarker(mouseEvent.latLng)
        })

        const addMarker = (position) => {
            // 클릭 이벤트를 통해서 들어오는 position 정보를 이용하여 마커 생성
            const marker = new kakao.maps.Marker({
                position
            })
            markers.push(marker)    // markers 리스트에 marker를 하나씩 넣어준다. push는 파이썬의 append랑 비슷.
            // 마커를 맵에 표시
            marker.setMap(map)
            console.log(markers)
        }
    </script>
</body>
</html>
```

우리는 세명이서 모일 경우에 가장 공평한 위치를 찾는게 목적이므로, 위에서 새로 만든 마커 위치 리스트에 위치가 딱 세개만 들어가도록 수정한다. `index.html` 수정.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <div id="map" style="width:500px;height:400px;"></div>
    <script type="text/javascript" src="http://dapi.kakao.com/v2/maps/sdk.js?appkey=앱키"></script>
    <script>
        let container = document.querySelector('#map'); //지도를 담을 영역의 DOM 레퍼런스
        let options = { //지도를 생성할 때 필요한 기본 옵션
            center: new kakao.maps.LatLng(33.450701, 126.570667), //지도의 중심좌표.
            level: 3 //지도의 레벨(확대, 축소 정도)
        };

        let map = new kakao.maps.Map(container, options); //지도 생성 및 객체 리턴
        const markers = []

        // 카카오 맵에 이벤트 리스너 등록
        kakao.maps.event.addListener(map, 'click', function(mouseEvent) {
            addMarker(mouseEvent.latLng)
        })

        const addMarker = (position) => {
            // 클릭 이벤트를 통해서 들어오는 position 정보를 이용하여 마커 생성
            const marker = new kakao.maps.Marker({
                position
            })
            markers.push(marker)    // markers 리스트에 marker를 하나씩 넣어준다. push는 파이썬의 append랑 비슷.
            // 마커를 맵에 표시
            marker.setMap(map)
            
            // 마지막 마커를 등록 후 3개가 넘었다면
            if (markers.length > 3) {
                // 첫번째 마커를 지도상에서 지운다
                markers[0].setMap(null)
                // 마커 목록에서도 첫번째 마커 정보를 지운다
                markers.shift()
            }
        }
    </script>
</body>
</html>
```

이제 세 지점의 중간 지점을 알려주는 버튼을 만든다. `index.html` 수정.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <div id="map" style="width:500px;height:400px;"></div>
    <button id="together">모여라!</button>
    <script type="text/javascript" src="http://dapi.kakao.com/v2/maps/sdk.js?appkey=앱키"></script>
    <script>
        let container = document.querySelector('#map'); //지도를 담을 영역의 DOM 레퍼런스
        let options = { //지도를 생성할 때 필요한 기본 옵션
            center: new kakao.maps.LatLng(33.450701, 126.570667), //지도의 중심좌표.
            level: 3 //지도의 레벨(확대, 축소 정도)
        };

        let map = new kakao.maps.Map(container, options); //지도 생성 및 객체 리턴
        const markers = []

        // 카카오 맵에 이벤트 리스너 등록
        kakao.maps.event.addListener(map, 'click', function(mouseEvent) {
            addMarker(mouseEvent.latLng)
        })

        const addMarker = (position) => {
            // 클릭 이벤트를 통해서 들어오는 position 정보를 이용하여 마커 생성
            const marker = new kakao.maps.Marker({
                position
            })
            markers.push(marker)    // markers 리스트에 marker를 하나씩 넣어준다. push는 파이썬의 append랑 비슷.
            // 마커를 맵에 표시
            marker.setMap(map)
            
            // 마지막 마커를 등록 후 3개가 넘었다면
            if (markers.length > 3) {
                // 첫번째 마커를 지도상에서 지운다
                markers[0].setMap(null)
                // 마커 목록에서도 첫번째 마커 정보를 지운다
                markers.shift()
            }
        }

        const togetherBtn = document.querySelector('#together')
        togetherBtn.addEventListener('click', () => {
            if (markers.length === 3) {
                console.log('모여라!!!')
            } else {
                console.log('마커가 세개가 아닙니다.')
            }
        })

    </script>
</body>
</html>
```

이제 세 점으로부터 길이가 같은, 삼각형의 외심을 구해야 한다.

원래 무슨 라이브러리? 암튼 뭐가 있는데 그걸 웹에서 쓸 수 없다고 한다 (제대로 못들었다;;).

그래서 강사님께서 직접 다 풀어서 쓰신 js코드를 사용한다.

[https://gist.github.com/edueric-hphk/be443f4bc7640e8b01b019db98b9b44b](https://gist.github.com/edueric-hphk/be443f4bc7640e8b01b019db98b9b44b)

이 코드를 html이랑 같은 폴더에 `circumcenter.js` 로 저장한다.

`index.html` 에서 위에 저장한 `circumcenter.js` 를 불러온다.

```html
...
<script type="text/javascript" src="http://dapi.kakao.com/v2/maps/sdk.js?appkey=앱키"></script>
<script src="./circumcenter.js"></script>
...
```

이제 버튼으로 외심을 구한다. `index.html` 수정.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <div id="map" style="width:500px;height:400px;"></div>
    <button id="together">모여라!</button>
    <script type="text/javascript" src="http://dapi.kakao.com/v2/maps/sdk.js?appkey=앱키"></script>
    <script src="./circumcenter.js"></script>
    <script>
        let container = document.querySelector('#map'); //지도를 담을 영역의 DOM 레퍼런스
        let options = { //지도를 생성할 때 필요한 기본 옵션
            center: new kakao.maps.LatLng(33.450701, 126.570667), //지도의 중심좌표.
            level: 3 //지도의 레벨(확대, 축소 정도)
        };

        let map = new kakao.maps.Map(container, options); //지도 생성 및 객체 리턴
        const markers = []
        // 중심 마커를 저장할 수 잇는 변수 선언
        let centerMarker

        // 카카오 맵에 이벤트 리스너 등록
        kakao.maps.event.addListener(map, 'click', function(mouseEvent) {
            addMarker(mouseEvent.latLng)
        })

        const addMarker = (position) => {
            // 클릭 이벤트를 통해서 들어오는 position 정보를 이용하여 마커 생성
            const marker = new kakao.maps.Marker({
                position
            })
            markers.push(marker)    // markers 리스트에 marker를 하나씩 넣어준다. push는 파이썬의 append랑 비슷.
            // 마커를 맵에 표시
            marker.setMap(map)
            
            // 마지막 마커를 등록 후 3개가 넘었다면
            if (markers.length > 3) {
                // 첫번째 마커를 지도상에서 지운다
                markers[0].setMap(null)
                // 마커 목록에서도 첫번째 마커 정보를 지운다
                markers.shift()
            }
        }

        const togetherBtn = document.querySelector('#together')
        togetherBtn.addEventListener('click', () => {
            if (markers.length === 3) {
                // 마커는 getPosition 함수로 좌표를 가져올 수 있다
                // Ha: 위도, Ga: 경도
                // 세 개의 마커의 x, y 좌표를 이용해 외심을 구한다
                const center = circumcenter([
                    [markers[0].getPosition().Ha, markers[0].getPosition().Ga],
                    [markers[1].getPosition().Ha, markers[1].getPosition().Ga],
                    [markers[2].getPosition().Ha, markers[2].getPosition().Ga]
                ])
                // 계산된 중심의 좌표(center)를 카카오맵에서 사용가능한 객체로 저장
                const position = new kakao.maps.LatLng(center[0], center[1])
                // 만약 이미 중심 마커가 있다면 제거
                if (centerMarker) {
                    centerMarker.setMap(null)
                }
                // 중심 좌표를 이용해 중심 마커 생성
                centerMarker = new kakao.maps.Marker({
                    position
                })

                /*
                자바스크립트의 object는 파이썬의 dictionary와 비슷한 구조.
                근데 key과 value가 같으면 같이 써줘도 된다.
                즉,
                { 'position': position }
                이면 그냥
                { position }
                으로 써주면 된다.
                */

                // 중심 마커 등록
                centerMarker.setMap(map)

            } else {
                console.log('마커가 세개가 아닙니다.')
            }
        })

    </script>
</body>
</html>
```



# Chrome Extension 중 Momentum 만들기

`js_momentum` 폴더를 만들어서 그 안에 `momentum.html` 을 만든다.

```bash
mkdir js_momentum
cd js_momentum
touch momentum.html
```

`momentum.html` 에 기본 골격을 잡아주고 axios와 unsplash를 이용한다.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
    <script>
        axios.get('https://source.unsplash.com/1600x900')
    </script>
</body>
</html>
```

* [axios](https://github.com/axios/axios) 와 [unsplash](https://source.unsplash.com/) 이용

console log로 내가 원하는 자료를 어떻게 얻을 수 있나 본다. `momentum.html` 수정.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
    <script>
        axios.get('https://source.unsplash.com/1600x900')
            .then(response => {
                console.log(response)
            })
    </script>
</body>
</html>
```

* console log 살펴보면 내가 원하는 정보(이미지 주소)는  responseURL 에 있다는 걸 알 수 있다

이제 이미지를 배경에 넣는다. `momentum.html` 수정.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
    <script>
        axios.get('https://source.unsplash.com/1920x1080')
            .then(response => {
                const imgUrl = response.request.responseURL
                document.body.style.backgroundImage = `url(${imgUrl})`
            })
    </script>
</body>
</html>
```

시간을 넣는다. 일단 시간이 어떻게 가져와지는지 콘솔을 통해서 본다. `momentum.html` 수정.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
    <script>
        axios.get('https://source.unsplash.com/1920x1080')
            .then(response => {
                const imgUrl = response.request.responseURL
                document.body.style.backgroundImage = `url(${imgUrl})`
            })
        
        const getTime = function () {
            const now = new Date()
            console.log(now)
        }

        getTime()

    </script>
</body>
</html>
```

콘솔에 나온대로 각 요소를 불러온다. `momentum.html` 수정.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <div id="time"></div>
    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
    <script>
        axios.get('https://source.unsplash.com/1920x1080')
            .then(response => {
                const imgUrl = response.request.responseURL
                document.body.style.backgroundImage = `url(${imgUrl})`
            })
        
        const getTime = function () {
            const now = new Date()
            hours = now.getHours()
            minutes = now.getMinutes()
            seconds = now.getSeconds()
            if (hours > 12) {
                hours -= 12
                ampm = '오후 '
            } else {
                ampm = '오전 '
            }
            if (hours < 10) {
                hours = '0' + hours
            }
            if (minutes < 10) {
                minutes = '0' + minutes
            }
            if (seconds < 10) {
                seconds = '0' + seconds
            }
            document.querySelector('#time').innerHTML = ampm + hours + ':' + minutes + ':' + seconds
        }

        getTime()

    </script>
</body>
</html>
```

* getTime등으로 불러오는 결과는 자료형이 숫자이다
* 근데 '0'+숫자 가 가능하다.
* 자바스크립트에서는 숫자에 string을 더하면 string으로 변해서 string을 더하듯이 된다

시간이 계속 바뀌도록 수정한다. `momentum.html` 수정.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <div id="time"></div>
    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
    <script>
        axios.get('https://source.unsplash.com/1920x1080')
            .then(response => {
                const imgUrl = response.request.responseURL
                document.body.style.backgroundImage = `url(${imgUrl})`
            })
        
        const getTime = function () {
            const now = new Date()
            hours = now.getHours()
            minutes = now.getMinutes()
            seconds = now.getSeconds()
            if (hours > 12) {
                hours -= 12
                ampm = '오후 '
            } else {
                ampm = '오전 '
            }
            if (hours < 10) {
                hours = '0' + hours
            }
            if (minutes < 10) {
                minutes = '0' + minutes
            }
            if (seconds < 10) {
                seconds = '0' + seconds
            }
            document.querySelector('#time').innerHTML = ampm + hours + ':' + minutes + ':' + seconds
        }

        setInterval(getTime, 1000)

    </script>
</body>
</html>
```

bootstrap을 쓰기 위해 코드를 붙여넣는다. `momentum.html` 수정.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
</head>
<body>
    <div id="time"></div>
    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
    <script>
        axios.get('https://source.unsplash.com/1920x1080')
            .then(response => {
                const imgUrl = response.request.responseURL
                document.body.style.backgroundImage = `url(${imgUrl})`
            })
        
        const getTime = function () {
            const now = new Date()
            hours = now.getHours()
            minutes = now.getMinutes()
            seconds = now.getSeconds()
            if (hours > 12) {
                hours -= 12
                ampm = '오후 '
            } else {
                ampm = '오전 '
            }
            if (hours < 10) {
                hours = '0' + hours
            }
            if (minutes < 10) {
                minutes = '0' + minutes
            }
            if (seconds < 10) {
                seconds = '0' + seconds
            }
            document.querySelector('#time').innerHTML = ampm + hours + ':' + minutes + ':' + seconds
        }

        setInterval(getTime, 1000)

    </script>

    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</body>
</html>
```

디자인을 다듬는다. `momentum.html` 수정.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <style>
        html, body {
            width: 100%;
            height: 100%;
        }
        #parent {
            height: 100%;
        }
        #time {
            font-size: 5rem;    /* 5rem은 브라우저 기본 폰트 사이즈의 5배 */
        }
    </style>
</head>
<body>
    <div id="parent" class="d-flex justify-content-center align-items-center">
        <div id="time" class="text-light font-weight-bold"></div>
    </div>
    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
    <script>
        axios.get('https://source.unsplash.com/1920x1080')
            .then(response => {
                const imgUrl = response.request.responseURL
                document.body.style.backgroundImage = `url(${imgUrl})`
            })
        
        const getTime = function () {
            const now = new Date()
            hours = now.getHours()
            minutes = now.getMinutes()
            seconds = now.getSeconds()
            if (hours > 12) {
                hours -= 12
                ampm = '오후 '
            } else {
                ampm = '오전 '
            }
            if (hours < 10) {
                hours = '0' + hours
            }
            if (minutes < 10) {
                minutes = '0' + minutes
            }
            if (seconds < 10) {
                seconds = '0' + seconds
            }
            document.querySelector('#time').innerHTML = ampm + hours + ':' + minutes + ':' + seconds
        }

        setInterval(getTime, 1000)

    </script>

    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</body>
</html>
```

* flex는 flexible box ([추가 설명은 여기 참고](https://heropy.blog/2018/11/24/css-flexible-box/))



## 날씨 넣기

[https://openweathermap.org/](https://openweathermap.org/) 가입 후 api키를 가져온다.

https://openweathermap.org/api 에서 Current weather data 에 Subscribe 누르고 무료 플랜을 Get API key and Start 를 누른다.

API Call 부분을 복사해서 APPID 부분에 아까 내 api키를 넣는다.

완성된 API Call 주소를 주소창에 쳐보면 JSON형태로 정보가 표시된다 (근데 내 api key가 activate 될때까지 시간이 좀 걸린다).

근데 이건 우리가 원하는 위치의 날씨가 아니다.

그래서 [api doc](https://openweathermap.org/current)을 참고해서 서울 날씨를 찾는다.

`api.openweathermap.org/data/2.5/weather?q={city name}`  이렇게 하면 된다고 한다.

`api.openweathermap.org/data/2.5/weather?q=seoul&APPID={APIKEY}` 이렇게 쓴다.

이제 `momentum.html` 에 날씨를 넣는다.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <style>
        html, body {
            width: 100%;
            height: 100%;
        }
        #parent {
            height: 100%;
        }
        #time {
            font-size: 5rem;    /* 5rem은 브라우저 기본 폰트 사이즈의 5배 */
        }
    </style>
</head>
<body>
    
    <nav class="navbar justify-content-end fixed-top">
        <span id="weather"></span>
    </nav>
    
    <div id="parent" class="d-flex justify-content-center align-items-center">
        <div id="time" class="text-light font-weight-bold"></div>
    </div>

    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
    <script>
        axios.get('https://source.unsplash.com/1920x1080')
            .then(response => {
                const imgUrl = response.request.responseURL
                document.body.style.backgroundImage = `url(${imgUrl})`
            })
        
        const getTime = function () {
            const now = new Date()
            hours = now.getHours()
            minutes = now.getMinutes()
            seconds = now.getSeconds()
            if (hours > 12) {
                hours -= 12
                ampm = '오후 '
            } else {
                ampm = '오전 '
            }
            if (hours < 10) {
                hours = '0' + hours
            }
            if (minutes < 10) {
                minutes = '0' + minutes
            }
            if (seconds < 10) {
                seconds = '0' + seconds
            }
            document.querySelector('#time').innerHTML = ampm + hours + ':' + minutes + ':' + seconds
        }

        setInterval(getTime, 1000)

        const WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather?q=seoul&APPID=앱키'
        axios.get(WEATHER_API_URL)
            .then(res => {
                console.log(res)
            })

    </script>

    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</body>
</html>
```

* 콘솔 로그로 원하는 데이터를 찾는다.

원하는 데이터를 가져온다. `momentum.html` 수정.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <style>
        html, body {
            width: 100%;
            height: 100%;
        }
        #parent {
            height: 100%;
        }
        #time {
            font-size: 5rem;    /* 5rem은 브라우저 기본 폰트 사이즈의 5배 */
        }
    </style>
</head>
<body>
    
    <nav class="navbar justify-content-end fixed-top">
        <span id="weather" class="font-weight-bold text-light"></span>
    </nav>
    
    <div id="parent" class="d-flex justify-content-center align-items-center">
        <div id="time" class="text-light font-weight-bold"></div>
    </div>

    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
    <script>
        axios.get('https://source.unsplash.com/1920x1080')
            .then(response => {
                const imgUrl = response.request.responseURL
                document.body.style.backgroundImage = `url(${imgUrl})`
            })
        
        const getTime = function () {
            const now = new Date()
            hours = now.getHours()
            minutes = now.getMinutes()
            seconds = now.getSeconds()
            if (hours > 12) {
                hours -= 12
                ampm = '오후 '
            } else {
                ampm = '오전 '
            }
            if (hours < 10) {
                hours = '0' + hours
            }
            if (minutes < 10) {
                minutes = '0' + minutes
            }
            if (seconds < 10) {
                seconds = '0' + seconds
            }
            document.querySelector('#time').innerHTML = ampm + hours + ':' + minutes + ':' + seconds
        }

        setInterval(getTime, 1000)

        const weather = document.querySelector('#weather')
        const WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather?q=seoul&APPID=앱키&units=metric'
        axios.get(WEATHER_API_URL)
            .then(res => {
                const weatherCity = res.data.name
                const weatherData = res.data.weather[0].description
                const temperature = res.data.main.temp
                weather.innerText = `${temperature}°C ${weatherCity} ${weatherData}`
            })

    </script>

    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</body>
</html>
```

* 날씨 단위를 섭씨로 하기 위해 api주소에 `&units=metric` 붙인다.



# django + javascript

이전에 진행했던 프로젝트에서 이어서 할건데, 내가 결석했던 날이라 강사님 git에서 가져온다.

이전 프로젝트에서 만들었던 좋아요 버튼을 수정하려고 한다.

강사님 git을 가져와서 `django_form` 을 복사해서 내 폴더에 `django_form_2`로 붙여넣는다.

`django_form_2` 폴더에서 진행한다. 일단 기본 환경을 다 설치한다.

```bash
python -m venv venv
activate
pip install -r requirements.txt
python -m pip install --upgrade pip
pip install django-bootstrap-pagination
python manage.py migrate
python manage.py runserver
```

`myform` > `settings.py` 를 수정한다.

```python
...
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
)
...
```

* 회원가입 안되는거 수정한 것.

`articles` > `templates` > `articles` > `_article.html` 수정.

```html
<!-- articles/_article.html -->

<div class="card text-center mb-5">
    <div class="card-header">
        글 작성자: {{ article.user }}
    </div>
    <div class="card-body">
        <h5 class="card-title">글 제목: {{ article.title }}</h5>
        <p class="card-text">
            <a href="{% url 'articles:like' article.pk %}">
                {% if user in article.like_users.all %}
                    <i class="fas fa-heart like-button" data-id="{{ article.pk }}" style="color: red"></i>
                {% else %}
                    <i class="far fa-heart like-button" data-id="{{ article.pk }}" style="color: cadetblue"></i>
                {% endif %}
            </a>
            {{ article.like_users.all|length }}명이 이 글을 좋아합니다.<br>
            <a href="{% url 'articles:detail' article.pk %}">[DETAIL]</a>
        </p>
    </div>
</div>
```

* i class 에 like-button 추가
* data-id="{{ article.pk }}" 추가

axios를 쓰기 위해 `myform` > `templates` > `base.html` 의 head에 cdn을 넣는다.

```html
...

<head>
    ...
    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
    ...
</head>

...
```

`articles` > `templates` > `articles` > `index.html` 수정.

```html
{% extends 'base.html' %}
{% load bootstrap_pagination %}

{% block body %}
    <h1>Articles</h1>
    {% if user.is_authenticated %}
    <a href="{% url 'articles:create' %}">[NEW]</a>
    {% else %}
    <a href="{% url 'accounts:login' %}">[새 글을 작성하려면 로그인을 해주세요!]</a>
    {% endif %}
    
    {% for article in articles %}
        {% include 'articles/_article.html' %}
    {% endfor %}
    <div class="d-flex justify-content-center">
        {% bootstrap_paginate articles %}
    </div>

    <script>
        // 1. 각 게시글 별로 좋아요 버튼이 있으니 All로 다 가져와보자.
        const likeButtons = document.querySelectorAll('.like-button')

        likeButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault()
                console.log(e)
            })
        })
    </script>

{% endblock %}
```

* 맨 밑에 스크립트 부분 추가.
* 콘솔에서 보니까 dataset에 id를 가져오면 될것같다. 이게 아까 설정한 data-id이다.
* 근데 data-id = {{ article.pk }} 임을 잊지 말자.

`articles` > `templates` > `articles` > `index.html` 수정.

```html
{% extends 'base.html' %}
{% load bootstrap_pagination %}

{% block body %}
    <h1>Articles</h1>
    {% if user.is_authenticated %}
    <a href="{% url 'articles:create' %}">[NEW]</a>
    {% else %}
    <a href="{% url 'accounts:login' %}">[새 글을 작성하려면 로그인을 해주세요!]</a>
    {% endif %}
    
    {% for article in articles %}
        {% include 'articles/_article.html' %}
    {% endfor %}
    <div class="d-flex justify-content-center">
        {% bootstrap_paginate articles %}
    </div>

    <script>
        // 1. 각 게시글 별로 좋아요 버튼이 있으니 All로 다 가져와보자.
        const likeButtons = document.querySelectorAll('.like-button')

        likeButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault()
                const articleID = e.target.dataset.id

                axios.get(`/articles/${articleID}/like/`)
                    .then(res => {
                        console.log(res)
                    })
            })
        })
    </script>

{% endblock %}
```

* 이렇게 하면 axios의 응답값으로 html이 통채로 들어온다.
* 그게 아니라 내가 원하는 요소만 가져오고 싶다.

근데 그 전에 `_article.html` 수정

```html
<!-- articles/_article.html -->

<div class="card text-center mb-5">
    <div class="card-header">
        글 작성자: {{ article.user }}
    </div>
    <div class="card-body">
        <h5 class="card-title">글 제목: {{ article.title }}</h5>
        <p class="card-text">
            {% if user in article.like_users.all %}
                <i class="fas fa-heart like-button" data-id="{{ article.pk }}" style="color: red"></i>
            {% else %}
                <i class="far fa-heart like-button" data-id="{{ article.pk }}" style="color: cadetblue"></i>
            {% endif %}
            {{ article.like_users.all|length }}명이 이 글을 좋아합니다.<br>
            <a href="{% url 'articles:detail' article.pk %}">[DETAIL]</a>
        </p>
    </div>
</div>
```

* a tag를 삭제한다.

`articles` > `views.py` 수정.

```python
...
from django.http import HttpResponse, JsonResponse
...

...

def like(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    user = request.user # 요청을 보낸 유저
    
    # 해당 게시글에 좋아요를 누른 사람들 중에
    # user.pk를 가진 유저가 존재하면,
    if request.user.is_authenticated:
        if article.like_users.filter(pk=user.pk).exists():
            # user를 삭제하고 (좋아요를 취소)
            article.like_users.remove(user)
            liked = False
        else:
            article.like_users.add(user)
            liked = True
        context = {'liked': liked}
        return JsonResponse(context)
    return redirect("accounts:login")

...
```

이런 비동기적으로 주고받는 방법을 ajax 라고 한다.

이제 like를 누르면 하트가 빨갛게 변하게끔 수정한다.

`articles` > `templates` > `articles` > `index.html` 수정.

```html
...
axios.get(`/articles/${articleID}/like/`)
    .then(res => {
        if (res.data.liked) {
        	e.target.style.color = 'crimson'
        } else {
        	e.target.style.color = 'black'
        }
    })
...
```

axios의 get 방식을 post로 바꾼다.

`articles` > `templates` > `articles` > `index.html` 수정.

```html
{% extends 'base.html' %}
{% load bootstrap_pagination %}

{% block body %}
    <h1>Articles</h1>
    {% if user.is_authenticated %}
    <a href="{% url 'articles:create' %}">[NEW]</a>
    {% else %}
    <a href="{% url 'accounts:login' %}">[새 글을 작성하려면 로그인을 해주세요!]</a>
    {% endif %}
    
    {% for article in articles %}
        {% include 'articles/_article.html' %}
    {% endfor %}
    <div class="d-flex justify-content-center">
        {% bootstrap_paginate articles %}
    </div>

    <script>
        // 1. 각 게시글 별로 좋아요 버튼이 있으니 All로 다 가져와보자.
        const likeButtons = document.querySelectorAll('.like-button')

        likeButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault()
                const articleID = e.target.dataset.id
                
                axios.defaults.xsrfCookieName = 'csrftoken'
                axios.defaults.xsrfHeaderName = 'X-CSRFToken'
                axios.post(`/articles/${articleID}/like/`)
                    .then(res => {
                        if (res.data.liked) {
                            e.target.style.color = 'crimson'
                        } else {
                            e.target.style.color = 'black'
                        }
                    })
                    .catch (err => {
                        console.log(err)
                    })
            })
        })
    </script>

{% endblock %}
```



## 백엔드 개발자를 위한 Tip

백엔드 개발자들이 웹에서 쉽게 이것저것 확인할 수 있도록 돕는 툴을 설치하려고 한다.

우선 bash에서 django-debug-toolbar를 설치한다.

```bash
pip install django-debug-toolbar
```

`myform` > `settings.py` 수정.

```python
...

INSTALLED_APPS = [
    ...
    
    # debug_toolbar
    'debug_toolbar',
]

...

MIDDLEWARE = [
    ...
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

...

INTERNAL_IPS = [
    '127.0.0.1',
]
```

`myform` > `urls.py` 수정.

```python
...
from django.conf import settings
import debug_toolbar

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    ...
]
```

이렇게 하면 웹에서 이것저것 볼 수 있다.