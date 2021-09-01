from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(
        verbose_name='タグ', 
        max_length=50, 
        unique=True
        )

    good = models.IntegerField(default=0)

    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    def post_count(self):
        n = Post.objects.filter(tag = self).count()
        return n

    def __str__(self):
        return self.name

COLOR_CHOICE = (
    ('#FFFFFF', '白'),
    ('#CBFFD3', '黄緑'), 
    ('#B1F9D0', '緑'), 
    ('#EDFFBE', '黄色'), 
    ('#C2EEFF', '水色'), 
    ('#BAD3FF', '青'), 
    ('#DCC2FF', '紫'), 
    ('#FFBEDA', '赤'), 
    ('#FFC7AF', 'オレンジ'), 
    )

class Post(models.Model):
    # 自分で作るタイトル・サイトのURL・自分がつけるメモ・作った人・タグ・作成日・更新日・URLのOGPで取得した画像・色
    site_url = models.URLField(
        verbose_name='サイトのURL', 
        max_length=1000, 
        blank=False, 
        )

    title = models.CharField(
        verbose_name='タイトル', 
        max_length=1000,
        blank=False,
        )

    memo = models.TextField(
        verbose_name='メモ', 
        max_length=1000,
        blank=True,
        )

    author = models.ForeignKey(
        User, 
        on_delete=models.PROTECT, 
        blank=False,
        verbose_name='作成者', 
        )
        
    tag = models.ManyToManyField(
        Tag, 
        blank=False,
        verbose_name='タグ', 
        default='お気に入り',
        )
        
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)
    
    image = models.CharField(
        verbose_name='サイトのサムネイル', 
        max_length=2000,
        blank=True,
        )

    image_color = models.CharField(
        verbose_name='色', 
        max_length=100,
        choices = COLOR_CHOICE,
        default=('#FFFFFF', '白')
    )
    
    def __str__(self):
        return self.site_url


class Like(models.Model):
    tag = models.ForeignKey(Tag, verbose_name="タグ", on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name="Likeしたユーザー", on_delete=models.PROTECT)


class Contact(models.Model):
    # ログイン前のお問い合わせページ
    name = models.CharField(
        verbose_name='お名前', 
        max_length=100,
        blank=False,
        )

    mail = models.EmailField(
        verbose_name='メールアドレス',
        blank=False,
    )

    context = models.TextField(
        verbose_name='お問い合わせ内容', 
        max_length=2000,
        blank=False,
        )
    
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)

    def __str__(self):
        return self.name



class Opinion(models.Model):
    # ログイン後のお問い合わせページ
    name = models.CharField(
        verbose_name='お名前', 
        max_length=100,
        blank=False,
        )

    mail = models.EmailField(
        verbose_name='メールアドレス',
        blank=False,
    )

    context = models.TextField(
        verbose_name='お問い合わせ内容', 
        max_length=2000,
        blank=False,
        )
        
    user = models.ForeignKey(
        User, 
        on_delete=models.PROTECT, 
        blank=False,
        verbose_name='作成者', 
        )
    
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)

    def __str__(self):
        return self.name