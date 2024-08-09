var a = 3
var b = 2.5

/**
 * nhung gia tri false
 * 1) 0
 * 2) false
 * 3) NaN
 * 4) null
 * 5) ''
 * 6) undefined
 */

var ketQua = a > b && a > 0 && b > 0 
// console.log(ketQua)
var tenNhanVien = new String('Tu \'Phu Lam\'' )

if (ketQua) {
    alert('Chuan roi')
    console.log(tenNhanVien)
} else {
    alert('Sai cmnr')
}
