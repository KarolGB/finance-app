import { ReactNode } from "react";
import { Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { Link } from "expo-router";

interface AuthLayoutProps {
  subtitle: string;
  error?: string;
  footerPrompt: string;
  footerLinkText: string;
  footerHref: "/login" | "/register";
  children: ReactNode;
}

export function AuthLayout({
  subtitle,
  error,
  footerPrompt,
  footerLinkText,
  footerHref,
  children,
}: AuthLayoutProps) {
  return (
    <SafeAreaView className="flex-1 items-center justify-center bg-[#0A0D12]">
      <Text className="text-2xl text-white">FINANCE APP</Text>
      <Text className="my-8 text-white text-lg">{subtitle}</Text>

      {error ? (
        <Text className="text-red-500 text-center mb-4 px-6">{error}</Text>
      ) : null}

      <View className="w-full items-center gap-6">{children}</View>

      <Text className="text-white mt-8">
        {footerPrompt}{" "}
        <Link href={footerHref}>
          <Text className="text-blue-500">{footerLinkText}</Text>
        </Link>
      </Text>
    </SafeAreaView>
  );
}
