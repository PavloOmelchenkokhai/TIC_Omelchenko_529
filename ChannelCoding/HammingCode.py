import random


def string_to_binary(text):

    # Перетворення рядка у двійкову послідовність
    binary = ""

    for char in text:
        binary += format(ord(char), '08b')

    return binary


def binary_to_string(binary):

    # Перетворення двійкової послідовності назад у текст
    text = ""

    for i in range(0, len(binary), 8):
        byte = binary[i:i + 8]

        if len(byte) == 8:
            text += chr(int(byte, 2))

    return text


def encode_hamming_12_8(byte):

    # Код Геммінга (12,8)
    d = list(map(int, byte))

    code = [0] * 12

    code[2] = d[0]
    code[4] = d[1]
    code[5] = d[2]
    code[6] = d[3]
    code[8] = d[4]
    code[9] = d[5]
    code[10] = d[6]
    code[11] = d[7]

    code[0] = (code[2] + code[4] + code[6] + code[8] + code[10]) % 2
    code[1] = (code[2] + code[5] + code[6] + code[9] + code[10]) % 2
    code[3] = (code[4] + code[5] + code[6] + code[11]) % 2
    code[7] = (code[8] + code[9] + code[10] + code[11]) % 2

    return ''.join(map(str, code))


def add_error(code):

    # Додаємо одну випадкову помилку
    code = list(code)

    error_position = random.randint(0, 11)

    code[error_position] = '1' if code[error_position] == '0' else '0'

    return ''.join(code), error_position + 1


def detect_and_correct(code):

    # Пошук та виправлення помилки
    code = list(map(int, code))

    s1 = (code[0] + code[2] + code[4] + code[6] + code[8] + code[10]) % 2
    s2 = (code[1] + code[2] + code[5] + code[6] + code[9] + code[10]) % 2
    s3 = (code[3] + code[4] + code[5] + code[6] + code[11]) % 2
    s4 = (code[7] + code[8] + code[9] + code[10] + code[11]) % 2

    error_position = s1 * 1 + s2 * 2 + s3 * 4 + s4 * 8

    if error_position != 0:
        code[error_position - 1] ^= 1

    corrected = ''.join(map(str, code))

    return corrected, error_position


def decode_hamming_12_8(code):

    # Декодування назад у 8 біт
    data_bits = (
        code[2] +
        code[4] +
        code[5] +
        code[6] +
        code[8] +
        code[9] +
        code[10] +
        code[11]
    )

    return data_bits


def main():
    with open("sequence.txt", "r", encoding="utf-8") as file:
        sequences = [line.strip() for line in file if line.strip()]

    with open("results_hamming.txt", "w", encoding="utf-8") as file:

        for seq_num, sequence in enumerate(sequences, 1):

            file.write(f"\n=== Sequence {seq_num} ===\n")
            file.write(f"Original sequence:\n{sequence}\n\n")

            binary_sequence = string_to_binary(sequence)

            file.write("Binary sequence:\n")
            file.write(binary_sequence + "\n\n")

            encoded_full = ""
            error_full = ""
            corrected_full = ""
            decoded_binary = ""

            file.write("Hamming (12,8):\n\n")

            for i in range(0, len(binary_sequence), 8):
                byte = binary_sequence[i:i + 8]

                if len(byte) < 8:
                    byte = byte.ljust(8, '0')

                encoded = encode_hamming_12_8(byte)

                encoded_with_error, added_error_pos = add_error(encoded)

                corrected, found_error_pos = detect_and_correct(
                    encoded_with_error
                )

                decoded = decode_hamming_12_8(corrected)

                encoded_full += encoded
                error_full += encoded_with_error
                corrected_full += corrected
                decoded_binary += decoded

                file.write(f"Byte:              {byte}\n")
                file.write(f"Encoded:           {encoded}\n")
                file.write(f"With error:        {encoded_with_error}\n")
                file.write(f"Added error pos:   {added_error_pos}\n")
                file.write(f"Found error pos:   {found_error_pos}\n")
                file.write(f"Corrected:         {corrected}\n")
                file.write(f"Decoded:           {decoded}\n")
                file.write("\n")

            restored_text = binary_to_string(decoded_binary)

            file.write("FINAL RESULT:\n\n")
            file.write(f"Full encoded:\n{encoded_full}\n\n")
            file.write(f"With errors:\n{error_full}\n\n")
            file.write(f"Corrected:\n{corrected_full}\n\n")
            file.write(f"Decoded binary:\n{decoded_binary}\n\n")
            file.write(f"Restored text:\n{restored_text}\n\n")

    print("Результати збережено у results_hamming.txt")


if __name__ == "__main__":
    main()