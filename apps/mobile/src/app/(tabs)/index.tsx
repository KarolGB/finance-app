import { Text, TouchableOpacity, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { logout } from "@/stores/authStore";

export default function index() {
  return (
    <SafeAreaView>
      <Text>Main</Text>
      <TouchableOpacity className="text-black" onPress={logout}>
        <Text>Logout</Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
}
