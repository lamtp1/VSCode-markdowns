You can achieve this using a simple Python script. Here's an example:

        # Define the name
        name = 'Ethernet 9 - 9'

        # Split the name at the '-' character
        parts = name.split('-')

        # Remove any leading or trailing whitespace from the parts
        parts = [part.strip() for part in parts]

        # Join the first part (before the '-') back together
        new_name = ' '.join(parts[:1])

        # Open a text file for writing
        with open('output.txt', 'w') as f:
            # Write the new name to the text file
            f.write(new_name)


In this example, we define the name at the beginning of the script. We then split the string at the '-' character using the split method, remove any leading or trailing whitespace from the resulting parts, and join the first part (before the '-') back together using the join method.

Finally, we open a text file called "output.txt" for writing using the open function, and write the new name to the text file using the write method.

After running this script, the output.txt file will contain the following:

        Ethernet 9

Note that this script assumes that the name only contains a single '-' character. If there are multiple '-' characters in the name, you may need to modify the script to handle them correctly.