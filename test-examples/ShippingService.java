package com.example.service;

import org.springframework.stereotype.Service;
import java.time.LocalDate;

/**
 * 发货服务示例 - 用于测试业务规则检查
 */
@Service
public class ShippingService {
    
    /**
     * 发货方法 - 缺少商品实例校验（应该被检测到违规）
     */
    public void shipProduct(Long productId, String address) {
        // 直接发货，没有校验商品实例是否生效
        System.out.println("发货商品: " + productId);
        deliveryProduct(productId, address);
    }
    
    /**
     * 正确的发货方法 - 包含商品实例校验
     */
    public void shipProductWithValidation(Long productId, String address) {
        // 校验商品实例是否生效
        validateProductInstance(productId);
        
        // 执行发货
        deliveryProduct(productId, address);
    }
    
    /**
     * 月初发货方法 - 缺少子产品重复下发校验（应该被检测到违规）
     */
    public void monthlyShipment(Long productId) {
        LocalDate currentDate = LocalDate.now();
        if (currentDate.getDayOfMonth() <= 5) {
            // 月初发货，但没有检查是否已经下发过子产品
            shipProduct(productId, "default address");
        }
    }
    
    /**
     * 正确的月初发货方法 - 包含子产品校验
     */
    public void monthlyShipmentWithValidation(Long productId) {
        LocalDate currentDate = LocalDate.now();
        if (currentDate.getDayOfMonth() <= 5) {
            // 检查当月是否已经下发过子产品
            checkMonthlySubProductDelivered(productId, currentDate.getMonthValue());
            
            // 执行发货
            shipProductWithValidation(productId, "default address");
        }
    }
    
    /**
     * 商品实例状态更新 - 缺少业务规则校验（应该被检测到违规）
     */
    public void updateProductStatus(Long productId, String newStatus) {
        // 直接更新状态，没有业务规则校验
        System.out.println("更新商品状态: " + productId + " -> " + newStatus);
    }
    
    /**
     * 正确的状态更新方法 - 包含业务规则校验
     */
    public void updateProductStatusWithValidation(Long productId, String newStatus) {
        // 校验业务规则
        validateBusinessRule(productId, newStatus);
        
        // 更新状态
        System.out.println("更新商品状态: " + productId + " -> " + newStatus);
    }
    
    // 辅助方法
    private void validateProductInstance(Long productId) {
        // 校验商品实例是否生效
    }
    
    private void checkMonthlySubProductDelivered(Long productId, int month) {
        // 检查当月是否已经下发过子产品
    }
    
    private void validateBusinessRule(Long productId, String newStatus) {
        // 校验业务规则
    }
    
    private void deliveryProduct(Long productId, String address) {
        // 执行实际发货逻辑
    }
}
