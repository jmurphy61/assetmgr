package scene;

import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.control.ScrollPane;
import javafx.scene.layout.VBox;

import java.util.Collection;
import java.util.Map;

public interface SceneController {
    ScrollPane generatePane(Map<String, Node> nodes, Class layout);
    Parent getContent();
}
