package com.example.gpio_control;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.Switch;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {


    Button button1;
    Button button2;
    Button button3;
    Switch switch_1;
    Switch switch_2;
    TextView textView;
    ProgressBar progressBar;
    EditText config_string_box;
    Handler handler;
    private String IP_of_remote_host;
    private int PORT_of_reomte_host;
    private String Private_secret_key;
    private String task_1;
    private String task_2;
    private String task_3;
    private String task_4_sw;
    private String task_5_sw;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        button1 = findViewById(R.id.button1);
        button2 = findViewById(R.id.button2);
        button3 = findViewById(R.id.button3);
        switch_1 = findViewById(R.id.switch1);
        switch_2 = findViewById(R.id.switch2);
        textView = findViewById(R.id.textView);
        progressBar = findViewById(R.id.progressBar);
        config_string_box = findViewById(R.id.editText);

        load_configuration_from_data_base();
        host_port_existance_checker();
        check_if_first_run();
        assign_equal_button_names();
        load_switch_states_from_database();
    }

    public void task_1_event(View view) {
        send_task("bt", task_1, "impulse");
    }

    public void task_2_event(View view) {
        send_task("bt", task_2, "impulse");
    }

    public void task_3_event(View view) {
        send_task("bt", task_3, "impulse");

    }

    public void task_4_sw_event(View view) {
        boolean on = ((Switch) view).isChecked();

        if (on) {
            send_task("sw_1", task_4_sw, "on");
        } else {
            send_task("sw_1", task_4_sw, "off");
        }
    }

    public void task_5_sw_event(View view) {
        boolean on = ((Switch) view).isChecked();

        if (on) {
            send_task("sw_2", task_5_sw, "on");
        } else {
            send_task("sw_2", task_5_sw, "off");
        }
    }

    public void send_task(String interface_id, String task, String gpio_action) {
        HomeSmartClient task1 = new HomeSmartClient(IP_of_remote_host, PORT_of_reomte_host, Private_secret_key, task, gpio_action, textView, progressBar);
        progressBar.setVisibility(View.VISIBLE);
        task1.execute();
        if (!interface_id.equals("bt")) {
            wait_for_save_switch_state_approval(gpio_action, interface_id);
        }
    }

    public void add_new_config_string(View view) {
        if (config_string_box.getVisibility() == View.INVISIBLE) {
            config_string_box.setVisibility(View.VISIBLE);
        } else {
            if ((config_string_box.getText().toString()).equals("")) {
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
            save_string_to_data_base("TASK_4_SW", task_strings[3]);
            save_string_to_data_base("TASK_5_SW", task_strings[4]);
            load_configuration_from_data_base();
            assign_equal_button_names();
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
        button1.setText(format_task_string_to_button_name(task_1));
        button2.setText(format_task_string_to_button_name(task_2));
        button3.setText(format_task_string_to_button_name(task_3));
        switch_1.setText(format_task_string_to_button_name(task_4_sw));
        switch_2.setText(format_task_string_to_button_name(task_5_sw));
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
        task_4_sw = load_string_from_database("TASK_4_SW");
        task_5_sw = load_string_from_database("TASK_5_SW");
    }

    public void save_switch_1_state(String state) {
        save_string_to_data_base("SW_1_STATE", state);
    }

    public void save_switch_2_state(String state) {
        save_string_to_data_base("SW_2_STATE", state);
    }

    private void load_switch_states_from_database() {
        if (load_string_from_database("SW_1_STATE").equals("on")) {
            switch_1.setChecked(true);
        } else {
            switch_1.setChecked(false);
        }

        if (load_string_from_database("SW_2_STATE").equals("on")) {
            switch_2.setChecked(true);
        } else {
            switch_2.setChecked(false);
        }
    }

    private void wait_for_save_switch_state_approval(final String state, final String button_id) {
        handler = new Handler();
        Runnable r = new Runnable() {
            public void run() {
                if (textView.getText().equals("OK. Starting task ...")) {
                    if (button_id.equals("sw_1")) {
                        save_switch_1_state(state);
                    }
                    if (button_id.equals("sw_2")) {
                        save_switch_2_state(state);
                    }
                }
                load_switch_states_from_database();
            }
        };
        handler.postDelayed(r, 2000);
    }


}
