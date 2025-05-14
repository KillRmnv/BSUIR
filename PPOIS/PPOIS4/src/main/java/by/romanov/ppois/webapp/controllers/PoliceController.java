package by.romanov.ppois.webapp.controllers;

import io.micronaut.http.annotation.Controller;
import io.micronaut.http.annotation.Get;
import io.micronaut.views.View;

@Controller("/")
public class PoliceController {
    @Get
    @View("police/initial")
    public void index() {
    }
}