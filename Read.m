device = bluetooth("HC-06");
disp(device);
configureTerminator(device, "CR");
configureCallback(device, "terminator", @readSerial);

function readSerial(src,~)
    data = readline(src);
    disp(data);
end
