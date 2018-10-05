package scene;

import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.control.Button;
import javafx.scene.control.ScrollPane;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import util.Constants;

import java.util.LinkedHashMap;
import java.util.Map;

public class MainMenuScene implements SceneController {
    private final BorderPane root = new BorderPane();
    private final Map<String, Node> top_nodes = new LinkedHashMap<>();
    private final Map<String, Node> center_nodes = new LinkedHashMap<>();
    private final Map<String, Node> bottom_nodes = new LinkedHashMap<>();
    private final Map<String, Button> buttons = new LinkedHashMap<>();

    public MainMenuScene() {
        Button entrySceneBtn = new Button("Enter a New Item");
        entrySceneBtn.setOnAction(event -> {
            System.out.println("Switch to entry scene...");
            EntryScene entryScene = new EntryScene();
            entrySceneBtn.getScene().setRoot(entryScene.getContent());
        });
        center_nodes.put("entrySceneButton", entrySceneBtn);
        buttons.put("entrySceneButton", entrySceneBtn);

        Button querySceneBtn = new Button("Search the Database");
        querySceneBtn.setOnAction(event -> {
            System.out.println("Switch to query scene, not yet implemented...");
        });
        center_nodes.put("querySceneBtn", querySceneBtn);
        buttons.put("querySceneBtn", querySceneBtn);

        root.setPadding(Constants.STANDARD_INSETS);
        root.setCenter(generatePane(center_nodes, VBox.class));
    }

    @Override
    public Parent getContent() {
        return root;
    }

    @Override
    public ScrollPane generatePane(Map<String, Node> nodes, Class layout) {
        if (layout.equals(VBox.class)) {
            VBox vbox = new VBox();
            vbox.setSpacing(10.);
            vbox.setPadding(Constants.INNER_INSETS);

            if (!nodes.isEmpty()) {
                vbox.getChildren().addAll(nodes.values());
            }
            return new ScrollPane(vbox);
        } else if (layout.equals(HBox.class)) {
            HBox hbox = new HBox();
            hbox.setSpacing(10);
            hbox.setPadding(Constants.INNER_INSETS);

            if (!nodes.isEmpty()) {
                hbox.getChildren().addAll(nodes.values());
            }
            return new ScrollPane(hbox);
        } else {
            System.out.println("Unsupported layout class.");
            return null;
        }
    }
}
