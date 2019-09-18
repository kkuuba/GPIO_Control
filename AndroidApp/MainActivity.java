package com.example.homeapp;

import android.graphics.Color;
import android.os.Bundle;
import android.view.View;
import android.widget.ProgressBar;
import android.widget.Switch;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

    }


    public void open_fence_gate(View view) {

        TextView textView = findViewById(R.id.textView);
        ProgressBar progressBar = findViewById(R.id.progressBar);

        String private_key = "ASg453Jd3rdr43dfr4443dfsdf";

        HomeSmartClient task1 = new HomeSmartClient("80.54.73.236", 6555, private_key, "open_fence_gate", textView, progressBar);
        task1.execute();

    }


    public void open_garage_gate(View view) {

        TextView textView = findViewById(R.id.textView);
        Switch simpleSwitch = findViewById(R.id.simpleswitch);
        ProgressBar progressBar = findViewById(R.id.progressBar);
        boolean switchState = simpleSwitch.isChecked();

        String private_key = "ASg453Jd3rdr43dfr4443dfsdf";

        if (switchState) {

            HomeSmartClient task2 = new HomeSmartClient("80.54.73.236", 6555, private_key, "open_garage_gate", progressBar);
            task2.execute();

        } else {
            textView.setTextColor(Color.GRAY);
            textView.setText(getResources().getString(R.string.button_locked));
        }


    }
}
