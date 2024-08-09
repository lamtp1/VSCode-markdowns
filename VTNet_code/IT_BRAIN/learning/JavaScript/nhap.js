var firstName = 'Tu'
var middleName = 'Phu'
var lastName = 'Lam'

// setTimeout(function() {
//     prompt(firstName + ' ' + middleName + ' ' + lastName)
// }, 10000)

// if (firstName == lastName) {
//     console.log('DUNG')
// } else {
//     console.log('SAI')
// }

var a = 4
var myName = 'Lamtp1'
var isFailed = false
var cnttDepartment
var b = null

function inConsoleLog(ten_nv) {
    console.log('Hello ae P.CNTT, t là ' + ten_nv + '!')
} 

function inCanhBao(canh_bao){
    alert(canh_bao + ' anh bạn à ' +'!')
}

var newFunction = function(lenh) {
    console.log('Hello ae P.CNTT, t là ' + lenh + '!')
}

var doiTuong = {
    ten: 'Lamtp1',
    ma_vn: 428118,
    phong_ban: 'P.CNTT',
    HAY: 12,
}

var arrayMoi = [
    13,
    34,
    'RTX 3060',
    'ATI'
]

setTimeout(newFunction, 2000, 'james harden')

if (myName == 'Lamtp1' && isFailed == true) {
    setTimeout(inConsoleLog, 3000, 'lamtp1')
} else {
    setInterval(inCanhBao, 5000, 'Nguy hiểm lắm')
}

console.log(doiTuong)
console.log(arrayMoi)