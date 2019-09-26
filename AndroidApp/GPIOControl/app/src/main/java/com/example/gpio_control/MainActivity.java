package com.example.gpio_control;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    private String IP_of_remote_host;
    private int PORT_of_reomte_host;
    private String Private_secret_key;
    private String task_1;
    private String task_2;
    private String task_3;
    private String task_4;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        load_configuration_from_data_base();
        host_port_existance_checker();
        check_if_first_run();
        assign_equal_button_names();

    }

    public void task_1_event(View view) {

        TextView textView = findViewById(R.id.textView);
        ProgressBar progressBar = findViewById(R.id.progressBar);
        HomeSmartClient task1 = new HomeSmartClient(IP_of_remote_host, PORT_of_reomte_host, Private_secret_key, task_1, "impulse", textView, progressBar);
        progressBar.setVisibility(View.VISIBLE);
        task1.execute();

    }

    public void task_2_event(View view) {

        TextView textView = findViewById(R.id.textView);
        ProgressBar progressBar = findViewById(R.id.progressBar);
        HomeSmartClient task1 = new HomeSmartClient(IP_of_remote_host, PORT_of_reomte_host, Private_secret_key, task_2, "impulse", textView, progressBar);
        progressBar.setVisibility(View.VISIBLE);
        task1.execute();

    }

    public void task_3_event(View view) {

        TextView textView = findViewById(R.id.textView);
        ProgressBar progressBar = findViewById(R.id.progressBar);
        HomeSmartClient task1 = new HomeSmartClient(IP_of_remote_host, PORT_of_reomte_host, Private_secret_key, task_3, "impulse", textView, progressBar);
        progressBar.setVisibility(View.VISIBLE);
        task1.execute();

    }

    public void task_4_event(View view) {

        TextView textView = findViewById(R.id.textView);
        ProgressBar progressBar = findViewById(R.id.progressBar);
        HomeSmartClient task1 = new HomeSmartClient(IP_of_remote_host, PORT_of_reomte_host, Private_secret_key, task_4, "impulse", textView, progressBar);
        progressBar.setVisibility(View.VISIBLE);
        task1.execute();

    }


    public void add_new_config_string(View view) {

        EditText config_string_box = findViewById(R.id.editText);

        if (config_string_box.getVisibility() == View.INVISIBLE) {
            config_string_box.setVisibility(View.VISIBLE);
        } else {
            if ((config_string_box.getText().toString()).equals("")) {
                TextView textView = findViewById(R.id.textView);
                textView.setText(getString(R.string.config_box_empty));
            } else {
                extract_and_save_data_from_config_string(config_string_box.getText().toString());
                config_string_box.setVisibility(View.INVISIBLE);
            }
        }
    }

    private void extract_and_save_data_from_config_string(String config_string) {
        TextView textView = findViewById(R.id.textView);
        try {
            String[] config_parts = config_string.split("#@#");
            String[] task_strings = config_parts[3].split("###");
            save_string_to_data_base("IP", config_parts[0]);
            save_string_to_data_base("PORT", config_parts[1]);
            save_string_to_data_base("PRIVATE_KEY", config_parts[2]);
            save_string_to_data_base("TASK_1", task_strings[0]);
            save_string_to_data_base("TASK_2", task_strings[1]);
            save_string_to_data_base("TASK_3", task_strings[2]);
            save_string_to_data_base("TASK_4", task_strings[3]);
            load_configuration_from_data_base();
        } catch (Exception e) {
            e.printStackTrace();
            textView.setText(getString(R.string.bad_format_of_cfg));
        }
    }

    private void save_string_to_data_base(String key, String value) {
        SharedPreferences.Editor editor = getSharedPreferences("CONFIG_DATA", MODE_PRIVATE).edit();
        editor.putString(key, value);
        editor.apply();
    }

    private String load_string_from_database(String key) {
        SharedPreferences prefs = getSharedPreferences("CONFIG_DATA", MODE_PRIVATE);
        return prefs.getString(key, "No data");
    }

    private void check_if_first_run() {
        if (IP_of_remote_host.equals("No data")) {
            TextView textView = findViewById(R.id.textView);
            textView.setText(getString(R.string.first_run_string));
        }
    }

    private void host_port_existance_checker() {
        String port = load_string_from_database("PORT");
        if (port.equals("No data")) {
            PORT_of_reomte_host = 1111;
        } else {
            PORT_of_reomte_host = Integer.valueOf(load_string_from_database("PORT"));
        }
    }

    private void assign_equal_button_names() {

        Button button1 = findViewById(R.id.button1);
        Button button2 = findViewById(R.id.button2);
        Button button3 = findViewById(R.id.button3);
        Button button4 = findViewById(R.id.button4);

        button1.setText(format_task_string_to_button_name(task_1));
        button2.setText(format_task_string_to_button_name(task_2));
        button3.setText(format_task_string_to_button_name(task_3));
        button4.setText(format_task_string_to_button_name(task_4));

    }

    private String format_task_string_to_button_name(String task_string) {
        return task_string.replace("_", " ").toUpperCase();
    }

    private void load_configuration_from_data_base() {
        IP_of_remote_host = load_string_from_database("IP");
        Private_secret_key = load_string_from_database("PRIVATE_KEY");
        task_1 = load_string_from_database("TASK_1");
        task_2 = load_string_from_database("TASK_2");
        task_3 = load_string_from_database("TASK_3");
        task_4 = load_string_from_database("TASK_4");
    }


}
