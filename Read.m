

%USB Communication
usb = serialport("/dev/tty.usbmodem14101", 9600);
disp(usb);
configureTerminator(usb, "CR");
configureCallback(usb, "terminator", @readSerial);

%Bluetooth Communication
btooth = serialport("/dev/tty.HC-06", 9600);
disp(btooth);
configureTerminator(btooth, "CR");
configureCallback(btooth, "terminator", @readSerial)


%print result from respective connection
function readSerial(src,~)
    data = readline(src);
    disp(data);
end
