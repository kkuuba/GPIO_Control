package com.example.gpio_control;

import android.app.Activity;
import android.graphics.Color;
import android.os.AsyncTask;
import android.view.View;
import android.widget.ProgressBar;
import android.widget.TextView;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class HomeSmartClient extends AsyncTask<Void, Void, Void> {

    public TextView output_string;
    public ProgressBar progress_bar;
    public String output;
    private String target_device_ip;
    private int target_device_port;
    private String private_key;
    private String task_string;
    private Socket sock;
    private boolean all_previous_passed_with_success = true;
    private String receiver_msg;
    private String gpio_action_string;


    HomeSmartClient(String ip, int port, String key, String task, String gpio_action, TextView textView, ProgressBar progressBar) {

        target_device_ip = ip;
        target_device_port = port;
        private_key = key;
        task_string = task;
        output_string = textView;
        progress_bar = progressBar;
        gpio_action_string = gpio_action;
    }

    private void send_task_to_device() {
        this.check_if_network_interface_is_on();
        this.create_socket_and_try_connect_to_server();
        this.send_public_key_and_task_string();
        this.check_if_server_accepted_task();
    }


    private void check_if_network_interface_is_on() {
        if (this.all_previous_passed_with_success) {
            try {
                sock = new Socket("www.google.com", 443);
                sock.close();

            } catch (IOException e) {
                e.printStackTrace();
                this.save_exception_prompt("Turn on your internet");
            }
        }
    }

    private void create_socket_and_try_connect_to_server() {
        if (this.all_previous_passed_with_success) {
            try {
                sock = new Socket();
                sock.connect(new InetSocketAddress(this.target_device_ip, this.target_device_port), 1000);
            } catch (IOException e) {
                e.printStackTrace();
                this.save_exception_prompt("Cannot establish connection");
            }
        }
    }

    private void save_exception_prompt(String error_code) {

        this.output = error_code;
        this.all_previous_passed_with_success = false;
    }

    private void send_public_key_and_task_string() {
        if (this.all_previous_passed_with_success) {
            try {
                OutputStream os = sock.getOutputStream();
                OutputStreamWriter osw = new OutputStreamWriter(os);
                BufferedWriter bw = new BufferedWriter(osw);
                String msg_prompt = this.create_messege_string();
                bw.write(msg_prompt);
                bw.flush();
            } catch (IOException e) {
                e.printStackTrace();
                this.save_exception_prompt("Broken pipeline");
            }
        }

    }


    private String get_response_from_server() {
        if (this.all_previous_passed_with_success) {
            try {
                InputStream is = sock.getInputStream();
                InputStreamReader isr = new InputStreamReader(is);
                BufferedReader br = new BufferedReader(isr);
                this.receiver_msg = br.readLine();
                sock.close();
            } catch (IOException e) {
                e.printStackTrace();
                this.save_exception_prompt("Server is not responding");
            }
        }
        return this.receiver_msg;
    }

    private void check_if_server_accepted_task() {
        if (this.all_previous_passed_with_success) {
            if (this.get_response_from_server().equals("starting_task")) {
                output = "OK. Starting task ...";
            } else {
                this.save_exception_prompt("Something gone wrong");
            }
        }
    }

    private String update_public_key(String private_key) {
        String seconds = Long.toString(System.currentTimeMillis() / 1000 / 5);
        String mixed_string = seconds + "%$%" + private_key;
        return this.SHA256(mixed_string);
    }

    private String create_messege_string() {
        return this.update_public_key(this.private_key) + "@#@" + this.task_string + "@#@" + this.gpio_action_string;
    }

    private String SHA256(String input) {
        MessageDigest md = null;
        try {
            md = MessageDigest.getInstance("SHA-256");
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        }
        assert md != null;
        md.update(input.getBytes(StandardCharsets.UTF_8));
        byte[] digest = md.digest();
        StringBuilder sb = new StringBuilder();
        for (byte b : digest) {
            sb.append(String.format("%02x", b & 0xFF));
        }
        return sb.toString();
    }


    @Override
    protected Void doInBackground(Void... voids) {
        this.send_task_to_device();
        return null;
    }

    @Override
    protected void onPostExecute(Void result) {
        if (this.output.equals("OK. Starting task ...")) {
            this.progress_bar.setVisibility(View.INVISIBLE);
            this.output_string.setTextColor(Color.GREEN);
        } else {
            this.progress_bar.setVisibility(View.INVISIBLE);
            this.output_string.setTextColor(Color.RED);
        }
        this.output_string.setText(this.output);
        super.onPostExecute(result);
    }


}
