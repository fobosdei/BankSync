<template>
    <transition name="toast-fade">
        <div
            v-if="store.isShow"
            class="fixed inset-x-0 top-4 z-50 flex justify-center px-4 pointer-events-none"
        >
            <div
                class="pointer-events-auto max-w-xl w-full rounded-2xl border px-4 py-3 flex items-start gap-3 backdrop-blur-md shadow-lg"
                :class="variantClass"
                role="alert"
            >
                <div class="mt-1">
                    <span
                        class="inline-flex h-8 w-8 items-center justify-center rounded-full bg-white/80 shadow-sm"
                        :class="iconCircleClass"
                    >
                        <span v-if="store.dialogType === 'success'">✓</span>
                        <span v-else-if="store.dialogType === 'danger'">!</span>
                        <span v-else-if="store.dialogType === 'warning'">!</span>
                        <span v-else>i</span>
                    </span>
                </div>
                <div class="flex-1">
                    <p class="text-sm font-semibold" :class="titleClass">
                        {{ store.dialogContent.title }}
                    </p>
                    <p class="text-sm text-gray-700 mt-0.5">
                        {{ store.dialogContent.firstLine }}
                    </p>
                    <p v-if="store.dialogContent.secondLine" class="text-xs text-gray-500 mt-1">
                        {{ store.dialogContent.secondLine }}
                    </p>
                </div>
            </div>
        </div>
    </transition>
</template>

<script setup>
import { computed } from 'vue';
import { useDialogStore } from '../store/dialog';

const store = useDialogStore();

const variantClass = computed(() => {
    switch (store.dialogType) {
        case 'success':
            return 'bg-green-50/90 border-green-200 shadow-green-200/70';
        case 'danger':
            return 'bg-red-50/90 border-red-200 shadow-red-200/70';
        case 'warning':
            return 'bg-yellow-50/90 border-yellow-200 shadow-yellow-200/70';
        case 'info':
        default:
            return 'bg-blue-50/90 border-blue-200 shadow-blue-200/70';
    }
});

const titleClass = computed(() => {
    switch (store.dialogType) {
        case 'success':
            return 'text-green-800';
        case 'danger':
            return 'text-red-800';
        case 'warning':
            return 'text-yellow-800';
        case 'info':
        default:
            return 'text-blue-800';
    }
});

const iconCircleClass = computed(() => {
    switch (store.dialogType) {
        case 'success':
            return 'text-green-700';
        case 'danger':
            return 'text-red-700';
        case 'warning':
            return 'text-yellow-700';
        case 'info':
        default:
            return 'text-blue-700';
    }
});
</script>

<style scoped>
.toast-fade-enter-active,
.toast-fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.toast-fade-enter-from,
.toast-fade-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>