package scene;

import com.healthmarketscience.jackcess.Column;
import com.healthmarketscience.jackcess.Cursor;
import com.healthmarketscience.jackcess.Database;
import com.healthmarketscience.jackcess.DatabaseBuilder;

import javafx.event.EventHandler;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.TextField;
import javafx.scene.control.ScrollPane;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.scene.text.Text;

import java.io.File;
import java.io.IOException;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.UUID;

import util.Constants;
import util.print.QRLabelPrinter;
import util.qr.QRCodeEncoder;

public class EntryScene implements SceneController {
    private final BorderPane root = new BorderPane();
    private final Map<String, Node> top_nodes = new LinkedHashMap<>();
    private final Map<String, Node> center_nodes = new LinkedHashMap<>();
    private final Map<String, Node> bottom_nodes = new LinkedHashMap<>();
    private final Map<String, Button> buttons = new LinkedHashMap<>();
    private final Map<String, TextField> text_fields = new LinkedHashMap<>();

    EntryScene() {
        System.out.println("EntryScene() called...");
        ComboBox<String> tableList = new ComboBox<>();
        Button addBtn = new Button("Add");

        File dbFile = new File("C:\\Users\\Jones Murphy\\IdeaProjects\\assetmgr\\src\\main\\resources\\inventory.accdb");
        System.out.println(dbFile.getPath());

        EventHandler handler = event -> {
                System.out.println("Populating text fields...");
                try {
                    if (root.getCenter() != null) {
                        ScrollPane center = (ScrollPane) root.getCenter();
                        VBox vbox = (VBox) center.getContent();
                        vbox.getChildren().removeAll(center_nodes.values());
                        root.setCenter(new ScrollPane(vbox));
                        text_fields.clear();
                        center_nodes.clear();
                    }

                    Database db = DatabaseBuilder.open(dbFile);
                    for (Column column : db.getTable(tableList.getValue()).getColumns()) {
                        String column_name = column.getName().toUpperCase();
                        switch (column_name) {
                            case Constants.ID:
                                System.out.println("This table has an ID field. Should auto increment.");
                                TextField IDField = new TextField();
                                Cursor cursor = db.getTable(tableList.getValue()).getDefaultCursor();
                                cursor.afterLast();

                                IDField.setText("ID");
                                IDField.setDisable(true);
                                text_fields.put(column_name, IDField);
                                center_nodes.put(column_name, IDField);
                                break;
                            case Constants.UUID:
                                System.out.println("This table supports UUID generation. Should auto assign.");
                                // Check previously assigned UUIDs for collision
                                TextField UUIDField = new TextField();
                                UUIDField.setPrefWidth(500);
                                UUIDField.setText(UUID.randomUUID().toString());
                                UUIDField.setDisable(true);
                                text_fields.put(column_name, UUIDField);
                                center_nodes.put(column_name, UUIDField);
                                break;
                            default:
                                System.out.println("Column: " + column_name);
                                System.out.println("Column data type: " + column.getType());
                                TextField textField = new TextField();
                                textField.setPromptText(column.getName());
                                text_fields.put(column_name, textField);
                                center_nodes.put(column_name, textField);
                                break;
                        }
                        root.setCenter(generatePane(center_nodes, VBox.class));
                    }
                    db.close();
                } catch (IOException e) {
                    System.out.println(String.format("Access DB file at the specified path (%s) does not exist.",
                            dbFile.getPath()));
                }
        };

        top_nodes.put(Constants.TABLE_LIST_PREFACE, new Text(Constants.TABLE_LIST_PREFACE_TEXT));
        tableList.getItems().add("Select a table...");
        try {
            Database db = DatabaseBuilder.open(dbFile);
            tableList.getItems().addAll(db.getTableNames());
            db.close();
        } catch (IOException e) {
            System.out.println(String.format("Access DB file at the specified path (%s) does not exist.",
                    dbFile.getPath()));
        }
        tableList.getSelectionModel().selectFirst();
        tableList.setOnAction(event -> handler.handle(event));
        top_nodes.put("tableList", tableList);
        addBtn.setOnAction(event -> {
            try {
                ArrayList<Object> values = new ArrayList<>();
                for (String key : text_fields.keySet()) {
                    switch(key) {
                        case Constants.ID:
                            values.add(Column.AUTO_NUMBER);
                            break;
                        case Constants.UUID:
                            values.add(text_fields.get(key).getText());
                            QRLabelPrinter.print(QRCodeEncoder.generate(text_fields.get(Constants.UUID).getText(),
                                    250,
                                    "png"));
                            break;
                        default:
                            values.add(text_fields.get(key).getText());
                    }
                }
                Database db = DatabaseBuilder.open(dbFile);
                db.getTable(tableList.getValue()).addRow(values.toArray());
                db.close();

                handler.handle(event);
            } catch (Exception e) {
                System.out.println("There was an exception: " + e.getMessage());
            }
        });
        buttons.put("addBtn", addBtn);
        bottom_nodes.put("addBtn", addBtn);

        Button mainMenuBtn = new Button("Back to Main Menu");
        mainMenuBtn.setOnAction(event -> {
            System.out.println("Switch to entry scene...");
            MainMenuScene mainMenuScene = new MainMenuScene();
            mainMenuBtn.getScene().setRoot(mainMenuScene.getContent());
        });
        bottom_nodes.put("mainMenuBtn", mainMenuBtn);
        buttons.put("mainMenuBtn", mainMenuBtn);

        root.setPadding(Constants.STANDARD_INSETS);
        root.setTop(generatePane(top_nodes, HBox.class));
        root.setCenter(generatePane(center_nodes, VBox.class));
        root.setBottom(generatePane(bottom_nodes, VBox.class));
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
