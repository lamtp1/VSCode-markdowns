package com.springlab01.quanlyvanban;

import java.util.ArrayList;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import com.springlab01.quanlyvanban.database.QlvbDB;
import com.springlab01.quanlyvanban.models.DmNguoiDung;

@SpringBootApplication
public class QuanlyvanbanApplication {

	public static void main(String[] args) {
		SpringApplication.run(QuanlyvanbanApplication.class, args);
		System.out.println("XIN CHAO Spring !!!");
		String Str = "GiangTD";
		System.out.println(String.format(Str, "%30s"));
		QlvbDB qlvbDB = new QlvbDB();
		// qlvbDB.getThongTinNguoiDung();
		ArrayList<DmNguoiDung> arrNguoiDungs = qlvbDB.getNguoiDungAll();
		System.out.println("Tong so nguoi dung: " + arrNguoiDungs.size());
		
	}

}
