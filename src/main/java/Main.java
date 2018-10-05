import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.image.Image;
import javafx.stage.Stage;
import scene.MainMenuScene;

public class Main extends Application {

    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(Stage primaryStage) {
        MainMenuScene mainMenuScene = new MainMenuScene();
        Scene scene = new Scene(mainMenuScene.getContent());
        primaryStage.getIcons().add(new Image(this.getClass().getResourceAsStream("img/database.png")));

        primaryStage.setTitle("Asset Management");
        primaryStage.setMaximized(true);
        primaryStage.setScene(scene);
        primaryStage.show();
    }
}
