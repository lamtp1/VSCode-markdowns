package com.springlab01.quanlyvanban.controllers;

import java.util.ArrayList;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import com.springlab01.quanlyvanban.database.QlvbDB;
import com.springlab01.quanlyvanban.models.DmNguoiDung;
@Controller
public class NguoidungController {
    @GetMapping("/nguoidung/index")
    public String index(final Model model) {
        QlvbDB qlvbDB = new QlvbDB();
        ArrayList<DmNguoiDung> arrNguoiDungs = qlvbDB.getNguoiDungAll();
    

    
}