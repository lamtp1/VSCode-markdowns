package com.springlab01.quanlyvanban.controllers;

import java.util.ArrayList;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;

import com.springlab01.quanlyvanban.database.QlvbDB;
import com.springlab01.quanlyvanban.models.DmNguoiDung;

@Controller
public class NguoiDungController {
  @GetMapping("/nguoidung/index") // đường dẫn trên url trình duyệt
  // ví dụ: http://localhost:8080/nguoidung/index
  public String index(final Model model) {
    QlvbDB qlvbDB = new QlvbDB();
    ArrayList<DmNguoiDung> arrNguoiDungs = qlvbDB.getNguoiDungAll();
    String strHello = "Xin chào thế giới!!!";
    model.addAttribute("attHello", strHello);
    model.addAttribute("arrUser", arrNguoiDungs);
    return "/nguoidung/index"; // thư mục chứa file index.html
  }

  @GetMapping("/nguoidung/create") // dùng để hiện thị trang /nguoidung/create
  public String create(final Model model) {
    DmNguoiDung dmNguoiDung = new DmNguoiDung();
    dmNguoiDung.setBlTrangThai(true);
    model.addAttribute("nguoidung", dmNguoiDung);
    return "/nguoidung/create";
  }

  @PostMapping("/nguoidung/create") // dùng để hứng, xử lý NguoiDung từ view /nguoidung/create gửi lên
  public String create(@ModelAttribute("nguoidung") DmNguoiDung dmNguoiDung, Model model) {

    QlvbDB qlvbDB = new QlvbDB();
    // kiểm tra người dùng tồn tại trước khi insert
    DmNguoiDung dmNguoiDungCheck = qlvbDB.getNguoiDungByMaNguoiDung(dmNguoiDung.getMaNguoiDung());
    if (dmNguoiDungCheck != null) {
      System.out.println("Người dùng có mã :" + dmNguoiDung.getMaNguoiDung() + " đã tồn tại!");
      model.addAttribute("errMsg", "Người dùng có mã :" + dmNguoiDung.getMaNguoiDung() + " đã tồn tại!");
      model.addAttribute("nguoidung", dmNguoiDung);
      return "/nguoidung/create";
    }

    if (dmNguoiDung.getBlTrangThai() == true) {
      dmNguoiDung.setTrangThai(1);
    } else {
      dmNguoiDung.setTrangThai(0);
    }
    System.out.println("Nguoi Dung:"
        + dmNguoiDung.getMaNguoiDung()
        + "," + dmNguoiDung.getTenNguoiDung()
        + "," + dmNguoiDung.getMatKhau()
        + "," + dmNguoiDung.getEmail()
        + "," + dmNguoiDung.getSoDienThoai()
        + "," + dmNguoiDung.getGioiTinh()
        + "," + dmNguoiDung.getMaPhongBan()
        + "," + dmNguoiDung.getBlTrangThai()
        + "," + dmNguoiDung.getTrangThai());

    qlvbDB.insertNguoiDung(dmNguoiDung);

    return "redirect:/nguoidung/index";
  }

  // Sửa người dùng:
  @GetMapping("/nguoidung/edit/{id}") // dùng để hiện thị trang /nguoidung/edit
  public String edit(@PathVariable(value = "id") String maNguoiDung, final Model model) {
    System.out.println("PathVariable id: " + maNguoiDung);
    QlvbDB qlvbDB = new QlvbDB();
    DmNguoiDung dmNguoiDung = qlvbDB.getNguoiDungByMaNguoiDung(maNguoiDung);
    if(dmNguoiDung.getTrangThai() == 1 ) {
      dmNguoiDung.setBlTrangThai(true);
    }
    else {
      dmNguoiDung.setBlTrangThai(false);
    }

    model.addAttribute("nguoidung", dmNguoiDung);
    return "/nguoidung/edit";
  }

  @PostMapping("/nguoidung/edit") // dùng để hứng, xử lý NguoiDung từ view /nguoidung/edit gửi lên
  public String edit(@ModelAttribute("nguoidung") DmNguoiDung dmNguoiDung, Model model) {

    if (dmNguoiDung.getBlTrangThai() == true) {
      dmNguoiDung.setTrangThai(1);
    } else {
      dmNguoiDung.setTrangThai(0);
    }

    System.out.println("Nguoi Dung EDIT:"
        + dmNguoiDung.getMaNguoiDung()
        + "," + dmNguoiDung.getTenNguoiDung()
        + "," + dmNguoiDung.getMatKhau()
        + "," + dmNguoiDung.getEmail()
        + "," + dmNguoiDung.getSoDienThoai()
        + "," + dmNguoiDung.getGioiTinh()
        + "," + dmNguoiDung.getMaPhongBan()
        + "," + dmNguoiDung.getBlTrangThai()
        + "," + dmNguoiDung.getTrangThai());

    QlvbDB qlvbDB = new QlvbDB();
    qlvbDB.updateNguoiDung(dmNguoiDung);

    return "redirect:/nguoidung/index";
  }

  //xóa người dùng:
  @GetMapping("/nguoidung/delete/{id}") // dùng thực hiện xóa người dùng
  public String delete(@PathVariable(value = "id") String maNguoiDung, final Model model) {
    System.out.println("PathVariable id: " + maNguoiDung);
    QlvbDB qlvbDB = new QlvbDB();
    qlvbDB.deleteNguoiDung(maNguoiDung);
    
    return "redirect:/nguoidung/index";
  }

}
