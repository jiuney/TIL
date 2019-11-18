// 01_callback_intro_2.js

/*

    일급객체는 아래 3가지 조건을 만족한다.
    1. 변수에 담을 수 있다.
    2. 인자로 전달할 수 있다.
    3. 반환값으로 전달할 수 있다.

*/

const fco = function () {    // 1. 변수 fco에 함수 저장
    return n => n + 1    // 3. return값이 익명 함수
}
console.log(fco)    // 2. fco라는 함수가 console.log()라는 함수의 인자로 전달됨.

// 도전과제: fco()를 이용해서 num_101에 101을 담아주세요.
const num_101 = fco()(101)