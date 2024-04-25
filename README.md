# Instagram Bot (v1.0)


- ΛΕΙΤΟΥΡΓΙΑ

accounts.py

1. Δημιουργεί αυτόματα λογαριασμό στο Instagram με συγκεκριμένα στοιχεία που δίνεις
2. Το Instagram έχει όριο λογαριασμών σε μια μέρα τους 2-3 αρα μπορεί να έχεις θέμα στην δημιουργία


comments.py

1. Συνδέεται στο λογαριασμό σου και σχολιάζει στον διαγωνισμό που έχεις δώσει
2. Τα σχόλια γίνονται σε random χρόνο για να μην φας ban
3. Καλό είναι να βαλεις αρκετά ονόματα να διαλέγει για tag

- ΒΗΜΑΤΑ

1. Κάνε εξαγωγή όλων των αρχείων στο .zip, σε ένα νέο απλό φάκελο
2. Συμπλήρωσε τα στοιχεία στο InfoTag.ini ή στο InfoAccount.ini
3. Κατέβασε το Chrome και την Python (https://phoenixnap.com/kb/how-to-install-python-3-windows)
4. Πήγαινε στο φάκελο που δημιουργήθηκε στο Βήμα 1
5. Πάτησε δεξί κλικ στο περιθώριο του αρχείου και άνοιξέ στο Τερματικό (cmd)
6. Άν έχει ανοίξει το Τερματικό, γράψε τις εντολές στο Βήμα 7
7.      pip install -r requirements.txt
        pip install --upgrade -r requirements.txt
        python3 comments.py ή python3 accounts.py
9. Κράτησε το Τερματικό ανοιχτό όσο εκτελείται το πρόγραμμα
10. Τερμάτισε την διαδικασία με Ctrl + C, στο Τερματικό

- ΠΡΟΣΟΧΗ

1. Υπάρχει περίπτωση να μην τρέξει με την πρώτη εκτέλεση
2. Πρέπει να απενεργοποιήσεις το 2 factor authentication στο λογαριασμό σου πριν το τρέξεις
3. Το Instagram έχει daily limit για comments τα >180, οπότε για ασφάλεια θα τρέχεις μέχρι 120
4. Αφού βάλεις το verification code, μπορεί να κολλήσει. Κλείσε την καρτέλα και άνοιξε κανονικά το λογαριασμό
