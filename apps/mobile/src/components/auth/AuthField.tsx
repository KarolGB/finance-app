import { Text, TextInput, TextInputProps, View } from "react-native";

interface AuthFieldProps extends TextInputProps {
  label: string;
  containerClassName?: string;
}

export function AuthField({
  label,
  containerClassName = "",
  ...inputProps
}: AuthFieldProps) {
  return (
    <View className={`w-[80%] gap-2 ${containerClassName}`}>
      <Text className="text-white">{label}</Text>
      <TextInput
        {...inputProps}
        className="placeholder:text-gray-600 border border-[#2D3542] rounded-xl p-4 text-white"
      />
    </View>
  );
}
