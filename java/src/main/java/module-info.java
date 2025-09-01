module com.poo.java {
    requires javafx.controls;
    requires javafx.fxml;
    requires java.base;
    
    opens com.poo.java to javafx.fxml;
    exports com.poo.java;
}
