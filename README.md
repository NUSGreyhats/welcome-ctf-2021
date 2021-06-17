# Welcome-CTF-2021

Best CTF in August 2021!

# For challenge creation

- At least 3 challenges for each of the categories (Except OSint)
  - Preferably of easy, medium and hard difficulties
- Things to include in challenge file
  - Dockerfile (Refer to the sample that is given in Templates, ping in the infrastructure chat if there is any issues)
  - Challenge file
  - Readme.md

# Things to include in ReadMe.md

| Things to include               | Example                                                                   |
| ------------------------------- | ------------------------------------------------------------------------- |
| Challenge Details               | `Caesar thought of the perfect cipher. Can you break it?`                 |
| Setup instructions              | `Step 1: run docker_build.sh ......`                                      |
| Possible hints                  | `Hint: What Caesar Cipher?`                                               |
| Key concepts                    | `Scripting`                                                               |
| Solution (Can also be a script) | `Write a script to brute force all the combinations of the caesar cipher` |
| Learning objectives             | `Learn about the Caesar Cipher`                                           |
| Flag                            | `greyhats{salad_is_great_but_cipher_is_not}`                              |

## How to add a challenge?

1. Create your own branch and commit to the branch
1. Make a pull request to merge the challenge (Skip this if you already have a PR)
   1. Add the correct labels accordingly (If unsure send it in the challenge creation chat)
1. After checking your request will be merged or changes will be requested
   1. If changes are requested, back to 1.
   1. If approved go to 4
1. You are done :D

# For challenge testing

- Download [Docker](https://www.docker.com/)
- Clone the repository using `git clone https://github.com/NUSGreyhats/welcome-ctf-2021.git`
- Go into the folder of the file you are testing
- Follow build instructions
- Test the challenge
    - Feedback the challenge onto the kanban board for each of the categories (Will be under Projects Tab of Github)
    - Follow the format that is given
- This will be used to track who has complete which challenges