device = bluetooth("HC-06");
disp(device);
configureTerminator(device, "CR");
configureCallback(device, "terminator", @readSerial);

usb = serialport("/dev/tty.usbmodem14101", 9600);
disp(usb);
configureTerminator(usb, "CR");
configureCallback(usb, "terminator", @readSerial);

function readSerial(src,~)
    data = readline(src);
    disp(data);
end



