echo -n 'nicolacucina;password' | faas-cli invoke iris-auth
echo -n '' | faas-cli invoke iris-load
echo -n '' | faas-cli invoke iris-train
echo -n 'custom;1.0,2.0,3.0,4.0' | faas-cli invoke iris-predict