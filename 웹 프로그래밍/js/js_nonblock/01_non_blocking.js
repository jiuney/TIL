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