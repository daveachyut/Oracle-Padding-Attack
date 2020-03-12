# Oracle-Padding-Attack

We all know that you don’t do your own crypto.

And even using someone else’s secure implementation of an encryption algorithm, with well-chosen secret keys and suchlike, is still open to brutally effective attacks.

My point is partly that you should never be complacent and should always be on the lookout for any way an attacker could gain any insight into your encryption, and partly that the Padding Oracle Attack is an incredibly cool demonstration of this.

Now, this vulnerability is not related to the Oracle database or the Oracle Company in any way.

In cryptography, a padding oracle attack is an attack which uses the padding validation of a cryptographic message to decrypt the ciphertext. The attack relies on having a "padding oracle" who freely responds to queries about whether a message is correctly padded or not.

Background Information:

There are two types of encryption schemes:

Symmetric key encryption: Encryption and decryption keys are the same.
Asymmetric key encryption: Encryption and decryption keys are not the same.

Symmetric cryptography:

In symmetric cryptography, the padding oracle attack can be applied to the CBC mode of operation, where the "oracle" (usually a server) leaks data about whether the padding of an encrypted message is correct or not. 

CBC Mode:

CBC, or Cipher-Block Chaining, encrypts plaintext by passing individual block of bytes (each character is a byte) of a fixed length through a “block cipher”, which uses a secret key to pretty much mess up the block beyond recognition. 

In CBC encryption, each block of plaintext is XORed with the previous ciphertext block before being passed into the cipher. According to Wikipedia it is “one of two block cipher modes recommended by Niels Ferguson and Bruce Schneier.”

In CBC mode, to make each message unique, an initialization vector (IV) is used in the first block. IV is sent along with the message in clear text format.

The preferred method of padding block ciphertexts is PKCS7. If the padding is 15 characters, you pad it with [01].

In simple terms, padding adds those extra few bits which are necessary before encryption to make a meaningful block.

The Padding Oracle Attack:

It turns out that knowing whether a given ciphertext produces plaintext with valid padding is ALL that an attacker needs to break a CBC encryption.

If we can submit ciphertexts and find out if they decrypt to something with valid padding, how do we use this fact to completely decrypt out stolen ciphertext?

Padding oracle attack on CBC encryption:

The standard implementation of CBC decryption in block ciphers is to decrypt all ciphertext blocks, validate the padding, remove the PKCS7 padding, and return the message's plaintext.

  

As depicted above, CBC decryption XORs each plaintext block with the previous ciphertext block. 

Suppose the attacker has two ciphertext blocks, and they want to decrypt the second block to get plaintext. The server then returns whether the padding of the last decrypted block is correct (equal to 0x01). At most, the attacker will need to make 256 attempts (one guess for every possible byte) to find the last byte of ciphertext. 

The intermediate state:

 

To repeat - in CBC encryption, each block of plaintext is XORed with the previous ciphertext block before being passed into the cipher.

This is the state of a ciphertext block after being decrypted by the block cipher but before being XORed with the previous ciphertext block.

We know C1 already, as it is just part of our ciphertext, so if we find I2 then we can trivially find P2 and decrypt the ciphertext.

 

Manipulating the ciphertext:

We exploit this by passing in C1' + C2, where C1' is a sneakily chosen ciphertext block, C2 is the ciphertext block we are trying to decrypt, and C1' + C2 is the concatenation of the two.

We pass C1' + C2 to the server.

 

After determining the last byte of ciphertext, the attacker can use the same technique to obtain the second-to-last byte of the ciphertext. The attacker then uses the same approach described above, this time modifying the second-to-last byte until the padding is correct (0x02, 0x02).

Attempting to bruteforce one block (16 bytes) at a time is significantly faster than the 2128 attempts required to bruteforce a 128-bit key.

Attacks using padding oracles:
Concrete instantiations of the attack were realised against SSL and IPSec in early 2000s. In 2012 it was shown to be effective against some hardened security devices.

As of early 2014, the attack is no longer considered a threat in real-life operation, though it is still workable in theory (see signal-to-noise ratio) against a certain class of machines. An attack called POODLE (late 2014) combines both a downgrade attack (to SSL 3.0) with a padding oracle attack on the older, insecure protocol to enable compromise of the transmitted data.
