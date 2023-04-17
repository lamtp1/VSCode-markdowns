package com.springlab01.quanlyvanban.controllers;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HomeController {
    
    @GetMapping("/index")
    public String index(final Model model)
    {
        return "index";
    }
}
