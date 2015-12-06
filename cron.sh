command="python /home/fernandosjp/Desktop/Fernando/GitHub/tesouro-investor/alert.py"
job="*/2 * * * * $command"
cat <(fgrep -i -v "$command" <(crontab -l)) <(echo "$job") | crontab -

