import { ActivityIndicator, Text, TouchableOpacity } from "react-native";

interface AuthButtonProps {
  title: string;
  isLoading: boolean;
  onPress: () => void;
}

export function AuthButton({ title, isLoading, onPress }: AuthButtonProps) {
  return (
    <TouchableOpacity
      className="w-[80%] mt-8 bg-blue-500 p-4 rounded-full"
      onPress={onPress}
      disabled={isLoading}
    >
      {isLoading ? (
        <ActivityIndicator color="white" />
      ) : (
        <Text className="text-center text-xl text-white">{title}</Text>
      )}
    </TouchableOpacity>
  );
}
