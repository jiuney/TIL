





기존에 만들었었던 `js` 폴더 안에 (아마 14일 수업때 만들었던 모양이다) `js_callback` 이라는 폴더를 만들어서 진행할 것.

```bash
mkdir js_callback
cd js_callback
```



```bash
touch 00_callback_intro_1.html
touch 01_callback_intro_2.js
```

00_callback_intro_1.html

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
    <button id="myButton">Click me</button>
    <script>
        const button = document.querySelector('#myButton')
        button.addEventListener('click', function() {
            console.log("button clicked!")
        })
    </script>
</body>
</html>
```

* d





01_callback_intro_2.js

```javascript

```







```console
setTimeout(function() {
  console.log("3초 후 출력된다!")
}, 3000)
```







비동기 = 일이 순차적으로 진행되지 않는다





03_google_dino.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <style>
        .bg {
            background-color: #f7f7f7;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
    </style>
</head>
<body>
    <div class="bg">
        <img
            id="dino"
            width="100px"
            height="100px"
            src="http://pixelartmaker.com/art/437771c87aeb56f.png" 
            alt="google-dino">
    </div>
    <div class="bg">
        <img
            id="dino-2"
            width="100px"
            height="100px"
            src="http://pixelartmaker.com/art/437771c87aeb56f.png" 
            alt="google-dino">
    </div>
    <script>
        const bg = document.querySelectorAll('.bg')
        console.log(bg)
    </script>
</body>
</html>
```



querySelector는 같은 이름을 가진 여러개 요소들 중에 첫번째만 가져온다

다 가져오고 싶으면 querySelectorAll 사용



03_google_dino.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <style>
        .bg {
            background-color: #f7f7f7;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
    </style>
</head>
<body>
    <div class="bg">
        <img
            id="dino"
            width="100px"
            height="100px"
            src="http://pixelartmaker.com/art/437771c87aeb56f.png" 
            alt="google-dino">
    </div>
    <script>
        const bg = document.querySelector('.bg')
        const dino = bg.querySelectorAll('#dino')
    </script>
</body>
</html>
```

* const로 뭔가를 가져오면 그의 자식까지 다 가져오게 된다
  * 그래서 bg.querySelector 가능













03_google_dino.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <style>
        .bg {
            background-color: #f7f7f7;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
    </style>
</head>
<body>
    <div class="bg">
        <img
            id="dino"
            width="100px"
            height="100px"
            src="http://pixelartmaker.com/art/437771c87aeb56f.png" 
            alt="google-dino">
    </div>
    <script>
        const bg = document.querySelector('.bg')
        const dino = bg.querySelector('#dino')
        dino.addEventListener('click', function() {
            console.log('아야!')
        })
    </script>
</body>
</html>
```





03_google_dino.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <style>
        .bg {
            background-color: #f7f7f7;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
    </style>
</head>
<body>
    <div class="bg">
        <img
            id="dino"
            width="100px"
            height="100px"
            src="http://pixelartmaker.com/art/437771c87aeb56f.png" 
            alt="google-dino">
    </div>
    <script>
        const bg = document.querySelector('.bg')
        const dino = bg.querySelector('#dino')
        document.addEventListener('keydown', function(event) {
            console.log('아야!')
            console.log(event)
        })
    </script>
</body>
</html>
```

* keydown은 키가 눌렸을 때 발생하는 이벤트



이벤트 객체 이용해서 조건 달기

03_google_dino.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <style>
        .bg {
            background-color: #f7f7f7;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
    </style>
</head>
<body>
    <div class="bg">
        <img
            id="dino"
            width="100px"
            height="100px"
            src="http://pixelartmaker.com/art/437771c87aeb56f.png" 
            alt="google-dino">
    </div>
    <script>
        const bg = document.querySelector('.bg')
        const dino = bg.querySelector('#dino')
        document.addEventListener('keydown', function(e) {
            if (e.key == ' ') {
                console.log('spacebar')
            } else if (e.key == "ArrowLeft") {
                console.log("left")
            } else if (e.key == "ArrowUp") {
                console.log("up")
            } else if (e.key == "ArrowDown") {
                console.log('down')
            } else {
                console.log('잘못된 key를 눌렀어요.')
            }
        })
    </script>
</body>
</html>
```



이벤트 객체 사용해서 공룡 움직이게 하기

03_google_dino.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <style>
        .bg {
            background-color: #f7f7f7;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
    </style>
</head>
<body>
    <div class="bg">
        <img
            id="dino"
            width="100px"
            height="100px"
            src="http://pixelartmaker.com/art/437771c87aeb56f.png" 
            alt="google-dino">
    </div>
    <script>
        const bg = document.querySelector('.bg')
        const dino = bg.querySelector('#dino')
        document.addEventListener('keydown', function(e) {
            if (e.key == ' ') {
                dino.style.marginLeft = '0px'
                dino.style.marginRight = '0px'
            } else if (e.key == "ArrowLeft") {
                dino.style.marginRight = '20px'
            } else if (e.key == "ArrowRight") {
                dino.style.marginLeft = '20px'
            } else if (e.key == "ArrowUp") {
                console.log("up")
            } else if (e.key == "ArrowDown") {
                console.log('down')
            } else {
                console.log('잘못된 key를 눌렀어요.')
            }
        })
    </script>
</body>
</html>
```

한번밖에 안움직이는거 수정.

03_google_dino.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <style>
        .bg {
            background-color: #f7f7f7;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
    </style>
</head>
<body>
    <div class="bg">
        <img
            id="dino"
            width="100px"
            height="100px"
            src="http://pixelartmaker.com/art/437771c87aeb56f.png" 
            alt="google-dino">
    </div>
    <script>
        const bg = document.querySelector('.bg')
        const dino = bg.querySelector('#dino')

        let x = 0
        let y = 0
        
        document.addEventListener('keydown', function(e) {
            if (e.key == ' ') {
                dino.style.marginLeft = '0px'
                dino.style.marginRight = '0px'
            } else if (e.key == "ArrowLeft") {
                x += 20
                dino.style.marginRight = `${x}px`
            } else if (e.key == "ArrowRight") {
                x += 20 
                dino.style.marginLeft = `${x}px`
            } else if (e.key == "ArrowUp") {
                y += 20
                dino.style.marginBottom = `${y}px`
            } else if (e.key == "ArrowDown") {
                y += 20
                dino.style.marginTop = `${y}px`
            } else {
                console.log('잘못된 key를 눌렀어요.')
            }
        })
    </script>
</body>
</html>
```





touch 04_shopping_list.html







04_shopping_list.html

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
    <h1>My Shopping List</h1>
    Enter a new item: <input id="item-input" type="text">
    <button id="add-button">Add Item</button>
    <ul id="shopping-list">
        
    </ul>
</body>
</html>
```





input창에 아이템을 입력하고 버튼을 누를때마다 밑에 목록에 추가되도록 하기.

04_shopping_list.html

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
    <h1>My Shopping List</h1>
    Enter a new item: <input id="item-input" type="text">
    <button id="add-button">Add Item</button>
    <ul id="shopping-list">
        
    </ul>
    <script>
        const input = document.querySelector('#item-input')
        const button = document.querySelector('#add-button')
        const shoppingList = document.querySelector('#shopping-list')

        button.addEventListener('click', function() {
            const itemName = input.value    // input 태그에 있는 값을 itemName 변수에 담아준다.
            const item = document.createElement('li')
            item.innerText = itemName
            shoppingList.append(item)
        })
    </script>
</body>
</html>
```

* script를 밑에 쓰는게 좋다. 왜냐면 순서대로 불러오기 때문에. html을 다 불러오고 나서 script를 불러오는게 사용자 입장에서 더 낫다 (그렇지 않으면 script를 다 불러오기 전까지는 빈 화면만 보고있어야 하기 때문에).



위의 상태로는 input창에 뭔가를 입력하고 나서 add item 버튼을 눌러도 input창에 기존 값이 그대로 남아있다.

add item 버튼을 클릭할때마다 input창이 비워지도록 하려면 다음과 같이 수정한다.

04_shopping_list.html

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
    <h1>My Shopping List</h1>
    Enter a new item: <input id="item-input" type="text">
    <button id="add-button">Add Item</button>
    <ul id="shopping-list">
        
    </ul>
    <script>
        const input = document.querySelector('#item-input')
        const button = document.querySelector('#add-button')
        const shoppingList = document.querySelector('#shopping-list')

        button.addEventListener('click', function() {
            const itemName = input.value    // input 태그에 있는 값을 itemName 변수에 담아준다.
            input.value = ''
            const item = document.createElement('li')
            item.innerText = itemName
            shoppingList.append(item)
        })
    </script>
</body>
</html>
```



item 삭제 버튼 추가.

04_shopping_list.html

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
    <h1>My Shopping List</h1>
    Enter a new item: <input id="item-input" type="text">
    <button id="add-button">Add Item</button>
    <button id="delete-button">Delete Item</button>
    <ul id="shopping-list">
        
    </ul>
    <script>
        const input = document.querySelector('#item-input')
        const button = document.querySelector('#add-button')
        const shoppingList = document.querySelector('#shopping-list')

        button.addEventListener('click', function() {
            const itemName = input.value    // input 태그에 있는 값을 itemName 변수에 담아준다.
            input.value = ''
            const item = document.createElement('li')
            item.innerText = itemName

            // Delete 버튼 추가
            const deleteButton = document.createElement('button')
            deleteButton.innerText = 'Delete'
            item.append(deleteButton)

            deleteButton.addEventListener('click', function() {
                item.remove()
            })

            shoppingList.append(item)
        })
    </script>
</body>
</html>
```

* 이 때 item이 여러개인데도 delete버튼이 오류없이 작동되는 이유는 deleteButton을 item의 자식으로 append해줬기 때문에 deleteButton이 동작할 때도 부모의 정보가 다 inherit되기 때문이다 (?)

























mkdir js_nonblock

cd js_nonblock

touch 00_blocking.py





00_blocking.py

```python
from time import sleep

def sleep_3s():
    sleep(3)
    print("wake up!")

print("Start sleeping")
sleep_3s()
print("End of Program")
```

실행 결과

```
Start sleeping
wake up!
End of Program
```









touch 01_non_blocking.js

01_non_blocking.js

```javascript
function sleep_3s() {
    setTimeout(() => console.log("Wake up!"), 3000)
}

console.log("Start sleeping")
sleep_3s()
console.log("End of Program")
```



실행

node 01_non_blocking.js



결과

```
Start sleeping
End of Program
wake up!
```

* 왜냐면 js는 sleep_3s()이 실행되는 3초를 안기다리고 (non-block) 바로 다음 코드를 실행해버리기 때문





01_non_blocking.js

```javascript
function sleep_3s() {
    setTimeout(() => console.log("Wake up!"), 3000)
}

console.log("Start sleeping")
sleep_3s()
console.log("End of Program")


function first() {
    console.log('first')
}

function second() {
    console.log('second')
}

function third() {
    console.log('third')
}

first()
setTimeout(second, 1000)    // 1초를 기다린 후에 second함수 실행
third()
```



실행 결과

```
first
third
second
```



javascript의 nonblocking 속성을 잘 기억해야 한다!





만약에 setTimeout을 0초로 한다면 어떻게 될까?

01_non_blocking.js

```javascript
...
first()
setTimeout(second, 1000)    // 1초를 기다린 후에 second함수 실행
third()
```

* 그래도 second가 마지막에 출력된다
  * 왜냐면 자바스크립트 내부 동작방식 때문.
  * [여기서](http://latentflip.com/loupe/?code=ZnVuY3Rpb24gZmlyc3QoKSB7CiAgICBjb25zb2xlLmxvZygnZmlyc3QnKQp9CgpmdW5jdGlvbiBzZWNvbmQoKSB7CiAgICBjb25zb2xlLmxvZygnc2Vjb25kJykKfQoKZnVuY3Rpb24gdGhpcmQoKSB7CiAgICBjb25zb2xlLmxvZygndGhpcmQnKQp9CgpmaXJzdCgpCnNldFRpbWVvdXQoc2Vjb25kLCAwKQp0aGlyZCgp!!!PGJ1dHRvbj5DbGljayBtZSE8L2J1dHRvbj4%3D) 코드 실행될 때 동작되는 순서를 볼 수 있는데, 여기서 볼 수 있듯이 setTimeout을 사용하면 그 안의 함수는 바로 call stack에 가는게 아니라 callback queue에서 대기하게 되고, call stack이 비어있을 때에야 call stack에 들어가게 된다. 그래서 second가 마지막에 출력되는 것.
  * stack은 last in first out (위에 쌓인게 먼저 나간다), queue는 first in first out (먼저 들어온게 먼저 나간다)
  * 가운데 동글뱅이 주황색 화살표 (이거 이름이 뭔지는 까먹음;;) 이게 의미하는 어떤 프로세스가 stack과 queue의 상태를 점검해서 stack이 비어있을 때 queue에 있는 것들을 넣어준다.





















다시 js_callback 폴더로 가서

touch 02_callback_function.js





02_callback_function.js

```javascript
const numbersEach = (numbers, callback) => {
    let acc    // accumulator 변수 생성
    for (const number of numbers) {
        acc = callback(number, acc)    // [???]한다 === callback
    }
    return acc
}



// 더한다
const addEach = (number, acc = 0) => {
    return acc + number
}

// 뺀다
const subtractEach = (number, acc = 0) => {
    return acc - number
}

// 곱한다
const multiplyEach = (number, acc = 1) => {
    return acc * number
}



const NUMBERS = [1, 2, 3, 4, 5]



console.log(numbersEach(NUMBERS, addEach))
console.log(numbersEach(NUMBERS, subtractEach))
console.log(numbersEach(NUMBERS, multiplyEach))
```







touch 03_axios.js



axios라는 라이브러리를 사용해볼 것.





npm install axios





axios는 api에 요청을 보낼 때 사용한다.



03_axios.js

```javascript
const axios = require('axios')

axios.get('https://jsonplaceholder.typicode.com/posts')
    .then(response => {
        console.log(response)
    })
    .catch(err => {
        console.log(err)
    })
```











브라우저에서도 axios 사용해보기



touch 04_dogs_and_cats.html



[github](https://github.com/axios/axios) 에서 CDN 가져와 body에 넣기



04_dogs_and_cats.html

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
    <h1>댕댕이</h1>
    <div class="animals"></div>
    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
</body>
</html>
```



브라우저에서 콘솔에서 사용해보기

콘솔

```
axios.get("https://dog.ceo/api/breeds/image/random")

axios.get("https://dog.ceo/api/breeds/image/random").then(response => console.log(response))
```





다시 돌아와서

04_dogs_and_cats.html

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
    <h1>댕댕이</h1>
    <div class="animals"></div>
    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
    <script>
        axios.get("https://dog.ceo/api/breeds/image/random")
            .then(response => {
                console.log(response)
                const imgUrl = response.data.message
            })
    </script>
</body>
</html>
```

이 때 브라우저에서 새로고침 했을 때 콘솔에 표시되는 정보에서 data의 message부분이 우리가 원하는 강아지 이미지의 url이다. 이를 바탕으로 다시 수정.

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
    <h1>댕댕이</h1>
    <div class="animals"></div>
    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
    <script>
        axios.get("https://dog.ceo/api/breeds/image/random")
            .then(response => {
                const imgUrl = response.data.message
                const imgTag = document.createElement('img')
                imgTag.src = imgUrl
                document.querySelector('.animals').append(imgTag)
            })
    </script>
</body>
</html>
```

이렇게 하면 새로고침 할때마다 강아지 사진이 랜덤으로 표시된다.





위 로직을 함수로 만들면

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
    <h1>댕댕이</h1>
    <div class="animals"></div>
    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
    <script>
        const getDogImage = () => {
            axios.get("https://dog.ceo/api/breeds/image/random")
                .then(response => {
                    const imgUrl = response.data.message
                    const imgTag = document.createElement('img')
                    imgTag.src = imgUrl
                    document.querySelector('.animals').append(imgTag)
                })
        }
    </script>
</body>
</html>
```

이렇게 하면 처음에는 강아지 사진이 표시 안되는데 콘솔에서

```
getDogImage()
```

를 실행하면, 실행할때마다 강아지 이미지가 와서 쌓인다. 이 때 중요한 점은 새로고침 안하고 적용된다는 점.





이번엔 버튼으로 만들기

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
    <h1>댕댕이</h1>
    <button id="dog">댕댕이 내놔</button>
    <div class="animals"></div>
    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
    <script>
        const getDogImage = () => {
            axios.get("https://dog.ceo/api/breeds/image/random")
                .then(response => {
                    const imgUrl = response.data.message
                    const imgTag = document.createElement('img')
                    imgTag.src = imgUrl
                    document.querySelector('.animals').append(imgTag)
                })
        }
        const dogButton = document.querySelector('#dog')
        dogButton.addEventListener('click', getDogImage)
    </script>
</body>
</html>
```







이번엔 고양이 사진도 불러오기

고양이 사진은 [여기서](https://docs.thecatapi.com/)

04_dogs_and_cats.html

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
    <h1>댕댕이 & 주인님</h1>
    <button id="dog">댕댕이 내놔</button>
    <button id="cat">주인님 내놔</button>
    <div class="animals"></div>
    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
    <script>
        const getDogImage = () => {
            axios.get("https://dog.ceo/api/breeds/image/random")
                .then(response => {
                    const imgUrl = response.data.message
                    const imgTag = document.createElement('img')
                    imgTag.src = imgUrl
                    document.querySelector('.animals').append(imgTag)
                })
        }
        const dogButton = document.querySelector('#dog')
        dogButton.addEventListener('click', getDogImage)

        const getCatImage = () => {
            axios.get("https://api.thecatapi.com/v1/images/search")
                .then(response => {
                    const imgUrl = response.data[0].url
                    const imgTag = document.createElement('img')
                    imgTag.src = imgUrl
                    document.querySelector('.animals').append(imgTag)
                })
        }
        const catButton = document.querySelector('#cat')
        catButton.addEventListener('click', getCatImage)
    </script>
</body>
</html>
```



























































































































































































































